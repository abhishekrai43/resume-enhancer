import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';

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

  errors: string[] = [];
  improvements: string[] = [];
  changes: { before: string; after: string }[] = [];
  downloadUrl: string = ''; 
  jobTitle: string = ''
  constructor(private http: HttpClient,private sanitizer: DomSanitizer,private router: Router) {}

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
          const fileName = this.selectedFile?.name || 'Unnamed File'; 
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
        this.ngOnInit(); 
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
      responseType: 'blob' 
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

  
enhanceResume() {
  if (!this.selectedResume) {
      this.showModal(' Please select a resume to enhance.');
      return;
  }

  if (!this.jobTitle || this.jobTitle.trim() === '') {
      this.showModal(' Please enter the job title before enhancing your resume.');
      return;
  }

  this.isEnhancing = true;

  const steps = [
    '🔍 Analyzing structure...',
    '📝 Checking spelling & grammar...',
    '🎨 Improving formatting...',
    ' Adding relevant keywords...',
    '✨ Finalizing enhancements...'
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

  //  Send Job Title to Backend
  const requestData = { job_title: this.jobTitle };

  this.http.post(`${this.apiUrl}/enhance/${this.selectedResume.id}`, requestData, {
      headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          "Content-Type": "application/json"
      },
      withCredentials: true
  }).subscribe({
      next: (response: any) => {
          // Debug: Log backend response
          console.log('Enhance response:', response);
          // Assign arrays directly from backend response
          this.errors = Array.isArray(response.errors) ? response.errors : [];
          this.improvements = Array.isArray(response.improvements) ? response.improvements : [];
          this.changes = Array.isArray(response.keywords) ? response.keywords : [];
          // Store analysis results immediately after enhancement, before any state reset
          localStorage.setItem('errors', JSON.stringify(this.errors));
          localStorage.setItem('improvements', JSON.stringify(this.improvements));
          localStorage.setItem('missingKeywords', JSON.stringify(this.changes));
          // Debug: Log what will be stored
          console.log('Errors to store:', this.errors);
          console.log('Improvements to store:', this.improvements);
          console.log('Keywords to store:', this.changes);
          // Store only arrays in localStorage
          localStorage.setItem('errors', JSON.stringify(this.errors));
          localStorage.setItem('improvements', JSON.stringify(this.improvements));
          localStorage.setItem('missingKeywords', JSON.stringify(this.changes));
          //  Store the correct file URL for downloading
          this.downloadUrl = response.file_url;

          this.isEnhancing = false;
          clearInterval(interval);

          // Store analysis results immediately after enhancement, before clearing state
          localStorage.setItem('errors', JSON.stringify(this.errors));
          localStorage.setItem('improvements', JSON.stringify(this.improvements));
          localStorage.setItem('missingKeywords', JSON.stringify(this.changes));
          //  Automatically trigger direct download after processing
          this.downloadEnhancedResume().then(() => {
              this.showModal("✨ Your Resume has been Awesomefied! ✨");
              setTimeout(() => {
                  this.resetEnhancementState();
              }, 1000);
          }).catch(() => {
              this.showModal("✨ Resume Enhanced! Check your downloads folder.");
              setTimeout(() => {
                  this.resetEnhancementState();
              }, 1000);
          });
      },
      error: (error) => {
          clearInterval(interval);
          console.error(' Failed to enhance resume:', error);
          this.showModal(' Enhancement failed.');
          this.isEnhancing = false;
          this.resetEnhancementState();
      }
  });
}

downloadEnhancedResume(): Promise<void> {
  return new Promise((resolve, reject) => {
      if (!this.downloadUrl) {
          this.showModal(" No enhanced resume available.");
          reject('No download URL');
          return;
      }

      const token = localStorage.getItem("access_token");
      if (!token) {
          this.showModal(" Authentication required. Please log in again.");
          reject('No token');
          return;
      }

      console.log("🔍 Downloading enhanced resume:", this.downloadUrl);

      //  Ensure the correct file is requested
      this.http.get(this.downloadUrl, {
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob' 
      }).subscribe({
          next: (blob) => {
              const link = document.createElement("a");
              link.href = window.URL.createObjectURL(blob);
              link.setAttribute("download", `enhanced_resume_${Date.now()}.pdf`); 
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              
              // Clean up the object URL
              setTimeout(() => {
                  window.URL.revokeObjectURL(link.href);
              }, 100);
              
              resolve();
          },
          error: (error) => {
              console.error(" Failed to download resume:", error);
              this.showModal(" Failed to download resume.");
              reject(error);
          }
      });
  });
}

// Reset enhancement state to allow selecting other resumes
resetEnhancementState() {
  // Clear previous enhancement data
  this.errors = [];
  this.improvements = [];
  this.changes = [];
  this.downloadUrl = '';
  this.jobTitle = '';
  this.enhancementStep = '';
  
  // Clear selected resume to allow fresh selection
  this.selectedResume = null;
  this.safePdfUrl = '';
}

// Function to close the modal
closeModal() {
  const modal = document.getElementById('analysisModal');
  if (modal) {
    modal.classList.remove('show');
  }
}

viewFullAnalysis() {
  // Only navigate, do NOT overwrite localStorage or clear state here
  this.router.navigate(['/analysis']);
}

  // Sign out the user
  signOut() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }

  // Delete Resume Function
  deleteResume(resumeId: number) {
    if (!confirm('Are you sure you want to delete this resume? This action cannot be undone.')) {
      return;
    }

    const token = localStorage.getItem('access_token');
    this.http.delete(`${this.apiUrl}/delete/${resumeId}`, {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: () => {
        // Remove from local array
        this.resumes = this.resumes.filter(r => r.id !== resumeId);
        this.showModal('Resume deleted successfully!');
        
        // Clear selection if deleted resume was selected
        if (this.selectedResume && this.selectedResume.id === resumeId) {
          this.selectedResume = null;
          this.safePdfUrl = '';
          this.errors = [];
          this.improvements = [];
          this.changes = [];
          this.downloadUrl = '';
        }
      },
      error: (error) => {
        console.error('Delete error:', error);
        this.showModal('Failed to delete resume. Please try again.');
      }
    });
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
