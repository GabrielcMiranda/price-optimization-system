import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { Button } from '../../../shared/components/button/button';
import { InputComponent } from '../../../shared/components/input/input';
import { Card } from '../../../shared/components/card/card';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, Button, InputComponent, Card],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login implements OnInit {
  loginForm!: FormGroup;
  isLoading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  get emailControl() {
    return this.loginForm.get('email');
  }

  get passwordControl() {
    return this.loginForm.get('password');
  }

  getEmailError(): string {
    if (this.emailControl?.hasError('required')) {
      return 'Email ou username é obrigatório';
    }
    return '';
  }

  getPasswordError(): string {
    if (this.passwordControl?.hasError('required')) {
      return 'Senha é obrigatória';
    }
    return '';
  }

  async onSubmit(): Promise<void> {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    try {
      const { email, password } = this.loginForm.value;
      console.log('Tentando login com:', email);
      await firstValueFrom(this.authService.login({ login: email, password }));
      console.log('Login bem-sucedido');
      this.isLoading = false;
      this.router.navigate(['/optimization']);
    } catch (error: any) {
      console.error('Erro no login:', error);
      this.errorMessage = error?.error?.detail || 'Erro ao fazer login. Verifique suas credenciais.';
      this.isLoading = false;
      this.cdr.detectChanges();
      console.log('isLoading definido como false, errorMessage:', this.errorMessage);
    }
  }
}
