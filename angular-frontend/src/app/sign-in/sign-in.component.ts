import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { CsrfTokenService } from '../csrf-token.service';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';


@Component({
  providers: [AuthService],
  selector: 'app-sign-in',
  imports: [ReactiveFormsModule],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})

export class SignInComponent {
  loginError: string | null = null;
  nextUrl: string = '/dashboard'

  signInForm = new FormGroup({
    username: new FormControl(),
    password: new FormControl(),
    re_password: new FormControl()
  })

  constructor(
    private authService: AuthService,
    private csrfTokenService: CsrfTokenService,
    private router: Router) { }

  ngOnInit(): void {
    this.csrfTokenService.fetchCsrfToken()
  }

  signIn(): void {
    const formValues = this.signInForm.value;
    const username = formValues.username;
    const password = formValues.password;

    this.authService.login(username, password).subscribe({
      next: () => this.router.navigateByUrl(this.nextUrl),
      error: (err) => {
        this.loginError = err.error?.message;
      }
    })
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
