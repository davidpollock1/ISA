import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { CsrfTokenService } from './csrf-token.service';


@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = '//localhost:8000'

  constructor(private http: HttpClient) { }


  login(username: string, password: string): Observable<any> {
    
    const body = { username, password };
    return this.http.post(`${this.apiUrl}/accounts/login`, body,  { withCredentials: true }
    );
  }

  register(username: string, password: string, re_password: string): Observable<any> {

    const body = { username, password, re_password };
    return this.http.post(`${this.apiUrl}/accounts/register`, body, { withCredentials: true})
  }

  logout(): void {
    // Perform any necessary cleanup and token removal
    this.removeAccessToken();
  }

  setAccessToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  removeAccessToken(): void {
    localStorage.removeItem('access_token');
  }

  isAuthenticated(): boolean {
    // Check if the user is authenticated based on your criteria (e.g., token existence)
    return !!this.getAccessToken();
  }
}
