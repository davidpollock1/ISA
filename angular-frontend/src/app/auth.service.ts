import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, catchError, map, Observable, of, tap } from 'rxjs';
import { environment } from '../environments/environment';
import { Router } from '@angular/router';

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface UserProfile {
  id: number;
  type: string;
  first_name: string;
  last_name: string;
  phone: string;
  city: string;
  email: string;
}

export interface CurrentUserResponse {
  isAuthenticated: boolean,
  user: User;
  profile: UserProfile;
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<CurrentUserResponse | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {
    this.checkCurrentUser().subscribe();
  }

  public isLoggedIn$ = this.currentUser$.pipe(
    map(user => !!user?.isAuthenticated)
  );

  checkCurrentUser(): Observable<CurrentUserResponse | null> {
    return this.http.get<CurrentUserResponse>(`${this.apiUrl}/accounts/currentuser/`, {
      withCredentials: true
    }).pipe(
      tap(response => this.currentUserSubject.next(response)),
      catchError(error => {
        this.currentUserSubject.next(null);
        return of(null);
      })
    );
  }

  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post(`${this.apiUrl}/accounts/login/`, body, {
      withCredentials: true
    }).pipe(
      tap(() => {
        this.checkCurrentUser().subscribe();
      })
    );
  }

  register(username: string, password: string, re_password: string): Observable<any> {
    const body = { username, password, re_password };
    return this.http.post(`${this.apiUrl}/accounts/register/`, body, {
      withCredentials: true
    });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/accounts/logout/`, {}, {
      withCredentials: true
    }).pipe(
      tap(() => {
        this.currentUserSubject.next(null);
        this.router.navigate(['/sign-in']);
      })
    );
  }
}
