import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { QuestionType } from './models';


@Component({
  selector: 'app-builder',
  imports: [ReactiveFormsModule],
  templateUrl: './builder.component.html',
  styleUrl: './builder.component.css',
  standalone: true
})
export class BuilderComponent {
  surveyForm = this.formBuilder.group({
    title: ['', Validators.required],
    internalName: ['', Validators.required],
    startDate: [null, Validators.required],
    endDate: [null, Validators.required],
    tags: [[''], Validators.required],
    questions: this.formBuilder.array([])
  })

  questionTypes: QuestionType[] = [
    { value: 'text', label: 'Short Answer' },
    { value: 'radio', label: 'Multiple Choice' },
    { value: 'checkbox', label: 'Checkboxes' }
  ];

  constructor(private formBuilder: FormBuilder) { }

  get questions(): FormArray {
    return this.surveyForm.get('questions') as FormArray;
  }

  newQuestion(): FormGroup {
    return this.formBuilder.group({
      label: ['', Validators.required],
      question: ['', Validators.required],
      type: ['text', Validators.required],
      options: this.formBuilder.array([])
    });
  }

  addQuestion() {
    this.questions.push(this.newQuestion());
  }

  removeQuestion(index: number) {
    this.questions.removeAt(index);
  }

  addOption(qIndex: number) {
    const options = this.questions.at(qIndex).get('options') as FormArray;
    options.push(this.formBuilder.control(''));
  }

  removeOption(qIndex: number, oIndex: number) {
    const options = this.questions.at(qIndex).get('options') as FormArray;
    options.removeAt(oIndex);
  }

  submit() {
    console.log(this.surveyForm.value);
  }
}
