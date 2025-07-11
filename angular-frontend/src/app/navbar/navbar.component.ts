import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { map, Observable } from 'rxjs';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone: false
})
export class NavbarComponent implements OnInit {
  isLoggedIn$: Observable<boolean>;

  constructor(private authService: AuthService) {
    this.isLoggedIn$ = this.authService.isLoggedIn$
  }
  ngOnInit(): void {
    this.authService.checkCurrentUser().subscribe();
  }

  logout() {
    this.authService.logout().subscribe();
  }
}
