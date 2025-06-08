import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-analysis',
  standalone: true,
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss'],
  imports: [CommonModule]
})
export class AnalysisComponent implements OnInit {
  errors: { error: string; explanation: string }[] = [];
  improvements: { suggestion: string; reason: string }[] = [];
  keywords: string[] = []; 

  constructor(private router: Router) {}

  ngOnInit() {
    // Retrieve stored analysis results from local storage
    const errorsData = localStorage.getItem('errors');
    const improvementsData = localStorage.getItem('improvements');
    const keywordsData = localStorage.getItem('missingKeywords');

    this.errors = errorsData ? JSON.parse(errorsData) : [];
    this.improvements = improvementsData ? JSON.parse(improvementsData) : [];
    this.keywords = keywordsData ? JSON.parse(keywordsData) : [];

    console.log('Errors loaded:', this.errors);
    console.log('Improvements loaded:', this.improvements);
    console.log('Keywords loaded:', this.keywords);
  }

  // Navigate back to the dashboard
  goBack() {
    this.router.navigate(['/dashboard']);
  }
}
