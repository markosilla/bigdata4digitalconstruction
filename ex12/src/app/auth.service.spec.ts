import { TestBed } from '@angular/core/testing';

import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  it('should update auth state when setAuthState is called', (done) => {
    service.authState$.subscribe(authState => {
      expect(authState).toBeTrue();
      done();
    });
    service.setAuthState(true);
  });

  it('isAuthenticated should return current auth state', () => {
    service.setAuthState(true);
    expect(service.isAuthenticated()).toBeTrue();
    service.setAuthState(false);
    expect(service.isAuthenticated()).toBeFalse();
  });

  it('logout should set auth state to false', (done) => {
    service.setAuthState(true);

    service.authState$.subscribe(authState => {
      expect(authState).toBeFalse();
      done();
    });

    // Spy on google.accounts.id.disableAutoSelect if available in global scope
    const googleObj = (window as any).google = {
      accounts: { id: { disableAutoSelect: jasmine.createSpy('disableAutoSelect') } }
    };

    service.logout();
    expect(googleObj.accounts.id.disableAutoSelect).toHaveBeenCalled();
  });
});
