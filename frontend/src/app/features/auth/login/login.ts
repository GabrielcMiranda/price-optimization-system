import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Button } from '../../../shared/components/button/button';
import { InputComponent } from '../../../shared/components/input/input';
import { Card } from '../../../shared/components/card/card';
import { LoadingSpinner } from '../../../shared/components/loading-spinner/loading-spinner';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, Button, InputComponent, Card, LoadingSpinner],
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
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
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
      return 'Email é obrigatório';
    }
    if (this.emailControl?.hasError('email')) {
      return 'Email inválido';
    }
    return '';
  }

  getPasswordError(): string {
    if (this.passwordControl?.hasError('required')) {
      return 'Senha é obrigatória';
    }
    if (this.passwordControl?.hasError('minlength')) {
      return 'Senha deve ter no mínimo 6 caracteres';
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
      await this.authService.login({ login: email, password }).toPromise();
      this.router.navigate(['/dashboard']);
    } catch (error: any) {
      this.errorMessage = error?.error?.detail || 'Erro ao fazer login. Verifique suas credenciais.';
    } finally {
      this.isLoading = false;
    }
  }
}
