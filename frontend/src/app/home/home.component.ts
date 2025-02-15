import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RegisterComponent } from '../components/register/register.component';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  imports: [CommonModule, FormsModule, RouterModule]
})
export class HomeComponent {
  showRegisterModal = false;
  registerComponent: any = null; // ✅ Correct variable name
  showModal = false;
  modalMessage = '';
  modalType: 'success' | 'error' = 'success';

  loginData = { email: '', password: '' }; 
  apiUrl = 'http://localhost:5001/auth/login'; 

  constructor(private router: Router, private http: HttpClient) {}

  async toggleRegisterModal() {
    this.showRegisterModal = !this.showRegisterModal;
    console.log(`Register Modal ${this.showRegisterModal ? "Opened" : "Closed"}`);

    if (!this.registerComponent) {
      try {
        const module = await import('../components/register/register.component');
        this.registerComponent = module.RegisterComponent;
      } catch (error) {
        this.showModalMessage("Error loading RegisterComponent", "error");
      }
    }
  }

  onLogin() {
    console.log("✅ Attempting Login...", this.loginData);

    if (!this.loginData.email || !this.loginData.password) {
      this.showModalMessage("Email and Password are required!", "error");
      return;
    }

    this.http.post(this.apiUrl, this.loginData).subscribe({
      next: (response: any) => {
        console.log("✅ Login Successful", response);
        localStorage.setItem("access_token", response.access_token);
        this.showModalMessage("Login successful! Redirecting to dashboard...", "success");
        setTimeout(() => this.router.navigate(['/dashboard']), 1500);
      },
      error: () => {
        this.showModalMessage("Invalid email or password. Please try again.", "error");
      }
    });
  }

  onRegisterSuccess() {
    this.showRegisterModal = false; 
    this.showModalMessage("Registration successful! You can now log in.", "success");
  }

  showModalMessage(message: string, type: 'success' | 'error') {
    this.modalMessage = message;
    this.modalType = type;
    this.showModal = true;
    setTimeout(() => this.showModal = false, 3000);
  }
}
