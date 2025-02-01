import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000'; // Flask Backend URL

  constructor(private http: HttpClient) {}

  // Fetch test message from Flask
  getTestMessage(): Observable<any> {
    return this.http.get(`${this.baseUrl}/auth/test`);
  }
}
