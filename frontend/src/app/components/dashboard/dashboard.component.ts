import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [CommonModule, FormsModule],
})
export class DashboardComponent implements OnInit {
  userName = '';
  profilePicData: string = '';
  selectedFile: File | null = null;
  resumes: any[] = [];
  selectedResume: any = null;
  isEnhancing = false;
  isLoading = false;
  enhancementStep = '';
  processedResumeUrl: string = '';
  apiUrl = 'http://localhost:5001/resume';
  safePdfUrl: SafeResourceUrl = '';
  // Add these properties for errors & improvements
  errors: string[] = [];
  improvements: string[] = [];
  changes: { before: string; after: string }[] = [];
  downloadUrl: string = ''; 
  constructor(private http: HttpClient,private sanitizer: DomSanitizer) {}

  ngOnInit() {
    const token = localStorage.getItem('access_token');
    this.isLoading = true;
    // Fetch profile
    this.http.get<any>(`${this.apiUrl}/user-profile`, {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: (data) => {
        this.userName = data.name;
        this.profilePicData = data.profile_pic ? `data:image/png;base64,${data.profile_pic}` : 'assets/profile-placeholder.png';
      },
      error: (error) => {
        console.error('Failed to load user profile:', error);
      }
    });

    // Fetch resumes
    this.http.get<any[]>(`${this.apiUrl}/user-resumes`, {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: (data) => {
        this.resumes = data;
        this.isLoading = false;
      },
      error: (error) => {
        this.showModal('Failed to load resumes:');
        this.isLoading = false;
      }
    });
  }

  // Handle profile picture upload
  onProfilePicSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('profile_pic', file);

    this.http.post(`${this.apiUrl}/upload-profile-pic`, formData, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
    }).subscribe({
      next: () => {
        this.profilePicData = URL.createObjectURL(file);
        this.showModal('Profile picture updated successfully!');
      },
      error: (error) => {
        console.error('Failed to upload profile picture:', error);
        this.showModal('Failed to upload profile picture.');
      }
    });
  }

  // Handle file selection for resume upload
  onFileSelected(event: any) {
    this.isLoading = true; 
    this.selectedFile = event.target.files[0];
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('resume_file', this.selectedFile);
      formData.append('title', this.selectedFile.name);
  
      this.http.post(`${this.apiUrl}/upload`, formData, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      }).subscribe({
        next: (data: any) => {
          const fileName = this.selectedFile?.name || 'Unnamed File'; // Safe access with fallback
          this.resumes.push({
            id: data.id,
            title: fileName,
            file_url: data.file_url
          });
      
          // Auto-select the uploaded file if present
          if (this.resumes.length > 0) {
            this.selectResume(this.resumes[this.resumes.length - 1]);
          }
          this.isLoading = false; 
        },
        error: (error) => {
          console.error('Failed to upload resume:', error);
          this.showModal('Failed to upload resume.');
          this.isLoading = false; 
        }
      });
    }
  }

  // Upload a new resume
  uploadResume() {
    if (!this.selectedFile) {
      this.showModal('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('resume_file', this.selectedFile);
    formData.append('title', this.selectedFile.name);

    this.http.post(`${this.apiUrl}/upload`, formData, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
    }).subscribe({
      next: () => {
        this.showModal('Resume uploaded successfully!');
        this.ngOnInit(); // Reload resumes
      },
      error: (error) => {
        console.error('Failed to upload resume:', error);
        this.showModal('Failed to upload resume.');
      }
    });
  }

  // Select a resume for preview
  selectResume(resume: any) {
    this.selectedResume = resume;
    this.isLoading = true
    const token = localStorage.getItem('access_token');

    this.http.get(`${this.apiUrl}/download/${resume.id}`, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob' // Ensure binary response
    }).subscribe({
      next: (blob) => {
        const pdfUrl = URL.createObjectURL(blob);
        this.safePdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(pdfUrl);
        this.isLoading = false
      },
      error: (error) => {
        this.showModal("Failed to load PDF:");
        this.isLoading = false
      }
    });
}

  
  // Enhance the selected resume with an animation

  enhanceResume() {
    if (!this.selectedResume) {
        this.showModal('Please select a resume to enhance.');
        return;
    }

    this.isEnhancing = true;

    // Enhancement Steps Animation
    const steps = [
      'Analyzing structure...',
      'Checking spelling...',
      'Improving formatting...',
      'Adding keywords...',
      'Finalizing...'
    ];

    let stepIndex = 0;
    this.enhancementStep = steps[stepIndex];

    const interval = setInterval(() => {
        stepIndex++;
        if (stepIndex < steps.length) {
            this.enhancementStep = steps[stepIndex];
        } else {
            clearInterval(interval);
        }
    }, 1500);

    // Call backend API
    this.http.post(`${this.apiUrl}/enhance/${this.selectedResume.id}`, {}, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            "Content-Type": "application/json"
        },
        withCredentials: true
    }).subscribe({
        next: (response: any) => {
            // Populate Errors, Improvements, and Changes
            this.errors = response.misspelled_words || [];
            this.improvements = response.improvements || [];
            if (Array.isArray(response.changes)) {
              this.changes = response.changes.map((change: any) => {
                if (typeof change === "string" && change.includes(" → ")) {
                  const [before, after] = change.split(" → ");
                  return { before: before.trim(), after: after.trim() };
                } else if (typeof change === "object" && change.before && change.after) {
                  return { before: change.before, after: change.after };
                }
                return { before: "Unknown", after: "Unknown" };
              });
            } else {
              this.changes = [];
            }
            
            this.downloadUrl = response.download_url;

            // ✅ Update PDF Viewer with enhanced resume
            if (this.downloadUrl) {
              const token = localStorage.getItem('access_token');
              console.log("Final Enhanced Resume URL:", this.downloadUrl);
              this.safePdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(`${this.downloadUrl}?token=${token}`);
            }
            

            // ✅ Show Completion Notification
            this.showModal("✨ Your Resume has been Awesomefied! ✨");

            this.isEnhancing = false;
        },
        error: (error) => {
            console.error('Failed to enhance resume:', error);
            this.showModal('Failed to enhance resume.');
            this.isEnhancing = false;
        }
    });
}

// Function to download enhanced resume
downloadEnhancedResume() {
  if (!this.downloadUrl) return;
 
  const token = localStorage.getItem('access_token');
  console.log("Download Token:", token);
  window.open(`${this.downloadUrl}?token=${token}`, "_blank");
}



  // Sign out the user
  signOut() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }
// Function to trigger file input click
triggerFileUpload() {
  (document.getElementById('fileInput') as HTMLInputElement)!.click();
}

  
  // Display a modal message
  showModal(message: string) {
    const modal = document.getElementById('customModal');
    const modalText = document.getElementById('modalText');
    if (modal && modalText) {
      modalText.innerText = message;
      modal.classList.add('show');

      setTimeout(() => {
        modal.classList.remove('show');
      }, 3000);
    }
  }
}
