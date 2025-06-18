import { Component, OnInit, NgZone } from '@angular/core';
import {AuthService} from '../auth.service';
import {Router} from '@angular/router';
import {jwtDecode} from 'jwt-decode';
declare const google: any;

@Component({
  selector: 'app-google-sign-in',
  templateUrl: './google-sign-in.component.html',
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
      callback: (response: any) => this.handleCredentialResponse(response)
    });

    google.accounts.id.renderButton(
      document.getElementById('google-signin-button'),
      { theme: 'outline', size: 'large' }  // customization attributes
    );

    google.accounts.id.prompt(); // also display the One Tap dialog
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
