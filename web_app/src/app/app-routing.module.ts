import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Import your components
import { QuizPageComponent } from './quiz-page/quiz-page.component';
import { HomeComponent } from './home/home.component';

// Define your routes
const routes: Routes = [
  {path : '' , component:HomeComponent},
{ path: 'quiz-page', component : QuizPageComponent },
{ path: '**', redirectTo: '' },
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
