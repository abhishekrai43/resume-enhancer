import { Component, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  imports: [CommonModule, FormsModule]
})
export class RegisterComponent {
  @Output() closeModal = new EventEmitter<void>(); // ✅ Event to close modal
  registerData = { name: '', email: '', password: '' };
  apiUrl = 'http://localhost:5001/auth/register';
  registrationSuccess = false; // ✅ Track modal visibility

  constructor(private http: HttpClient, private router: Router) {}

  onRegister() {
    console.log("✅ Register Clicked", this.registerData);

    if (!this.registerData.name || !this.registerData.email || !this.registerData.password) {
      alert("All fields are required!");
      return;
    }

    this.http.post(this.apiUrl, this.registerData).subscribe(
      (response: any) => {
        console.log("✅ User Registered Successfully", response);
        localStorage.setItem("access_token", response.access_token); // ✅ Store token

        this.registrationSuccess = true; // ✅ Show success modal
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error("❌ Registration failed", error);
        alert(error.error?.error || "Registration failed. Please try again.");
      }
    );
  }

  onSuccessModalOk() {
    this.closeModal.emit(); // ✅ Close Register Modal
    this.router.navigate(['/dashboard']); // ✅ Redirect to Dashboard
  }
}
