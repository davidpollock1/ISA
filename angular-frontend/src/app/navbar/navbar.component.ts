import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { map } from 'rxjs';

@Component({
    selector: 'app-navbar',
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css',
    standalone: false
})
export class NavbarComponent implements OnInit {
  currentUser$ = this.authService.currentUser$;
  isLoggedIn$ = this.authService.currentUser$.pipe(
    map(user => user !== null)
  );

  constructor(private authService: AuthService) { }
  ngOnInit(): void {

  }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  logout() {
    this.authService.logout().subscribe();
  }
}
