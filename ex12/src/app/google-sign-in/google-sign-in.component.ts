import { Component, OnInit, NgZone } from '@angular/core';
import {AuthService} from '../auth.service';
import {Router} from '@angular/router';
import {jwtDecode} from 'jwt-decode';
declare const google: any;

@Component({
  selector: 'app-google-sign-in',
  template: `
    <!--https://developers.google.com/identity/branding-guidelines-->
    <button class="gsi-material-button" (click)="onSignInClick()">
      <div class="gsi-material-button-state"></div>
      <div class="gsi-material-button-content-wrapper">
        <div class="gsi-material-button-icon">
          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block;">
            <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
            <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
            <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
            <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
            <path fill="none" d="M0 0h48v48H0z"></path>
          </svg>
        </div>
        <span style="display: none;">Sign in with Google</span>
      </div>
    </button>

  `,
  styleUrls: ['./google-sign-in.component.css']
})
export class GoogleSignInComponent implements OnInit {

  constructor(private ngZone: NgZone, private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.initializeGoogleSignIn();
  }

  initializeGoogleSignIn() {
    google.accounts.id.initialize({
      client_id: '387961159745-qq2a8virjuqp0207tgt1ithuv7bdqtdq.apps.googleusercontent.com',
      callback: (response: any) => this.handleCredentialResponse(response),
      use_fedcm_for_prompt: true,
      auto_select: false,            // Always show the account chooser
      ux_mode: 'popup'             // Popup allows inline selection
    });
  }

  onSignInClick() {
    google.accounts.id.prompt();
  }

  handleCredentialResponse(response: any) {
    const token = response.credential;
    const decoded: any = jwtDecode(token);

    // Send the token to your backend for verification
    // this.http.post('https://your-backend.com/api/auth/google', { token })
    //   .subscribe({
    //     next: (res) => {
    //       // Handle successful authentication
    //     },
    //     error: (err) => {
    //       // Handle errors
    //     }
    //   });



    console.log(decoded);

    // After successful verification with backend
    this.ngZone.run(() => {
      this.authService.setAuthState(true);
      // Navigate to a protected route, e.g.,
      this.router.navigate(['/dashboard']);
    });
  }
}
