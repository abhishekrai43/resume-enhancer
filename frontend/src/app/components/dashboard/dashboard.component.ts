import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

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
  enhancementStep = '';
  processedResumeUrl: string = '';
  apiUrl = 'http://localhost:5001/resume';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    const token = localStorage.getItem('access_token');

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
      },
      error: (error) => {
        console.error('Failed to load resumes:', error);
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
    this.selectedFile = event.target.files[0];
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
  }

  // Enhance the selected resume with an animation
  enhanceResume() {
    if (!this.selectedResume) {
      this.showModal('Please select a resume to enhance.');
      return;
    }

    this.isEnhancing = true;
    const steps = [
      'Analyzing structure...',
      'Improving grammar...',
      'Adding industry-specific keywords...',
      'Enhancing formatting...',
      'Finalizing AI-enhanced resume...'
    ];

    let stepIndex = 0;
    const interval = setInterval(() => {
      this.enhancementStep = steps[stepIndex];
      stepIndex++;

      if (stepIndex >= steps.length) {
        clearInterval(interval);
        this.isEnhancing = false;
        this.processedResumeUrl = `${this.apiUrl}/download/${this.selectedResume.id}`;
        this.showModal('Resume enhanced successfully!');
      }
    }, 1500);
  }

  // Sign out the user
  signOut() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
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
