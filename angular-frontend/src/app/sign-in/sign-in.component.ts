import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { CsrfTokenService } from '../csrf-token.service';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';


@Component({
  providers: [AuthService],
  selector: 'app-sign-in',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent {

  signInForm = new FormGroup({
    username: new FormControl(),
    password: new FormControl(),
    re_password: new FormControl()
  })


  constructor(
    private authService: AuthService,
    private csrfTokenService: CsrfTokenService) {}

  ngOnInit(): void {
    this.csrfTokenService.fetchCsrfToken()
  }

  signIn(): void {

    const formValues = this.signInForm.value;
    const username = formValues.username;
    const password = formValues.password;

    this.authService.login(username, password).subscribe(
      (success) => {
        if (success) {
          // whatever else we want to do when log in is successful. 
          console.log('Login Successful');
        } else {
          // whatever else we want to do when login fails
          console.log('Login failed');
        }
      },
      (error) => {
        console.log('Login Error:', error);
      }
    )
  }

  register(): void {

    const formValues = this.signInForm.value;
    const username = formValues.username;
    const password = formValues.password;
    const re_password = formValues.re_password;

    this.authService.register(username, password, re_password).subscribe(
      (success) => {
        if (success) {
          console.log('Registration Successful');
        } else {
          console.log('Registration failed');
        }
      },
      (error) => {
        console.log('Registration Error:', error);
      }
    )
  }
}
