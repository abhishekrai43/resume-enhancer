import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginData = { email: '', password: '' };
  apiUrl = 'http://localhost:5001/auth/login';

  constructor(private http: HttpClient, private router: Router) {}

  onLogin() {
    if (!this.loginData.email || !this.loginData.password) {
      alert("Email and password are required!");
      return;
    }
  
    this.http.post(this.apiUrl, this.loginData).subscribe({
      next: (response: any) => {
        localStorage.setItem("access_token", response.access_token); // Store JWT Token
        this.router.navigate(['/dashboard']).then(() => {
          window.location.reload();
        });
      },
      error: (error) => {
        console.error('❌ Login failed', error);
        alert(error.error?.error || 'Invalid email or password');
      }
    });
    
  }
  
}
