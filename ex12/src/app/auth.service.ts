import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
declare const google: any;

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authState = new BehaviorSubject<boolean>(false);
  authState$ = this.authState.asObservable();

  constructor() { }

  setAuthState(state: boolean) {
    this.authState.next(state);
  }

  isAuthenticated(): boolean {
    return this.authState.value;
  }

  logout() {
    this.authState.next(false);
    // Optionally, revoke the token
    google.accounts.id.disableAutoSelect();
    // Remove tokens from storage if stored
  }
}
