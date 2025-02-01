import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  imports: [CommonModule, FormsModule]
})
export class HomeComponent {
  showRegisterModal = false;

  toggleRegisterModal() {
    this.showRegisterModal = !this.showRegisterModal;
  }
}
