import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class QuestionService {
  private apiUrl = 'http://127.0.0.1:5000'; // Update with your Flask app URL

  constructor(private http: HttpClient) {}

  getQuestions(): Observable<any> {
    return this.http.get(`${this.apiUrl}/questions`);
  }

  // Assuming you have an endpoint in your Flask API to submit all answers
  submitAllAnswers(answers: any[]): Observable<any> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');

    // return this.http.post(`${this.apiUrl}/submit-all-answers`, { answers }, { headers });
    return this.http.post(`${this.apiUrl}/submit-all-answers`, { answers });
  }
}
