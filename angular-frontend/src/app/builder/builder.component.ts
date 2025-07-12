import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-builder',
  imports: [ReactiveFormsModule],
  templateUrl: './builder.component.html',
  styleUrl: './builder.component.css',
  standalone: true
})
export class BuilderComponent {
  form: FormGroup;

  constructor(private formBuilder: FormBuilder) {
    this.form = this.formBuilder.group({
      title: [''],
      questions: this.formBuilder.array([])
    })
  }

  get questions(): FormArray {
    return this.form.get('questions') as FormArray;
  }

  addQuestion() {
    const question = this.formBuilder.group({
      label: [''],
      type: ['text'],
      options: this.formBuilder.array([])
    });
    this.questions.push(question);
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
    console.log(this.form.value);
  }
}
