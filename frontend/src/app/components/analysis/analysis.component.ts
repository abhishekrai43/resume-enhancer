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
  keywords: string[] = []; // ✅ Fix keywords to string array

  constructor(private router: Router) {}

  ngOnInit() {
    // Retrieve stored analysis results from local storage
    const errorsData = localStorage.getItem('errors');
    const improvementsData = localStorage.getItem('improvements');
    const keywordsData = localStorage.getItem('missingKeywords');

    this.errors = errorsData ? JSON.parse(errorsData) : [];
    this.improvements = improvementsData ? JSON.parse(improvementsData) : [];
     // ✅ Ensure keywords are stored as an array of strings
  const rawKeywords = keywordsData ? JSON.parse(keywordsData) : [];
  
  this.keywords = rawKeywords.map((kw: any) => {
    // Ensure each keyword is extracted as a string
    return typeof kw === 'object' && kw.before && kw.after 
      ? `${kw.after}` 
      : String(kw);
  });

  console.log("Keywords Loaded:", this.keywords); // ✅ Debugging log

    // ✅ Remove `**asterisks**` from improvements
    this.improvements = this.improvements.map((imp: any) => ({
      suggestion: imp.suggestion.replace(/\*\*/g, ""), // Remove asterisks
      reason: imp.reason.replace(/\*\*/g, "") // Remove asterisks
    }));

    // ✅ Ensure `keywords` are just strings, NOT objects
    this.keywords = this.keywords.map((kw: any) => kw.toString());
  }

  // Navigate back to the dashboard
  goBack() {
    this.router.navigate(['/dashboard']);
  }
}
