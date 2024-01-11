// quiz-page.component.ts

import { Component, OnInit } from '@angular/core';
import { QuestionService } from './question.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-quiz-page',
  templateUrl: './quiz-page.component.html',
  styleUrls: ['./quiz-page.component.css'],
})
export class QuizPageComponent implements OnInit {
  questions: any[] = []; // Replace 'any' with your actual question type
  totalScore: number | undefined;
  showResultSection: boolean = false;
  constructor(private questionService: QuestionService, private http: HttpClient) {}

  ngOnInit(): void {
    this.loadRandomQuestions();
  }

  loadRandomQuestions() {
    this.questionService.getQuestions().subscribe((data) => {
      // Initialize 'answer' and 'score' properties for each question
      this.questions = this.shuffleArray(data).slice(0, 10).map((question) => ({
        ...question,
        answer: '',
        score: 0,
      }));
    });
  }

  shuffleArray(array: any[]): any[] {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  submitAllAnswers() {
    // Extract answers from questions
    const answers = this.questions.map((question) => ({
      questionId: question.id,
      answer: question.answer || '', // Use an empty string if 'answer' is undefined
    }));
  
    // Submit all answers to the server
    this.questionService.submitAllAnswers(answers).subscribe(
      (response: any) => {
        // Handle the response, which can include the predicted grades
        console.log('Full Response:', response);
  
        // Access the predictions if the structure is as expected
        const predictedGrades = response.predictions;
        console.log('Predicted Grades:', predictedGrades);
  
        // Update the score property for each question based on the predicted grade
        this.questions.forEach((question, index) => {
          question.score = Number(predictedGrades[index]);
        });
  
        // Calculate total score by summing up the scores
        this.totalScore = this.questions.reduce((sum, question) => sum + question.score, 0);
        console.log('Total Score:', this.totalScore);
      },
      (error) => {
        console.error('Error submitting answers:', error);
      }
    );
  
    // Set showResultSection to true after submitting answers
    this.showResultSection = true;
  }

  isAnswerCorrect(question: any, answer: string): boolean {
    
    return answer.trim() !== '';
  }

  showResult() {
    // Implement the logic to show the result, for example, an alert
    alert(`Total Score: ${this.totalScore}`);
  }
}
