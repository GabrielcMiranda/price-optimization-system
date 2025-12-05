import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Button } from '../../../shared/components/button/button';
import { InputComponent } from '../../../shared/components/input/input';
import { Card } from '../../../shared/components/card/card';
import { LoadingSpinner } from '../../../shared/components/loading-spinner/loading-spinner';
import { AuthService } from '../../../core/services/auth';

@Component({
  selector: 'app-register',
  imports: [CommonModule, ReactiveFormsModule, RouterModule, Button, InputComponent, Card, LoadingSpinner],
  templateUrl: './register.html',
  styleUrl: './register.scss',
})
export class Register implements OnInit {
  registerForm!: FormGroup;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (!password || !confirmPassword) {
      return null;
    }

    return password.value === confirmPassword.value ? null : { passwordMismatch: true };
  }

  get nameControl() {
    return this.registerForm.get('name');
  }

  get emailControl() {
    return this.registerForm.get('email');
  }

  get passwordControl() {
    return this.registerForm.get('password');
  }

  get confirmPasswordControl() {
    return this.registerForm.get('confirmPassword');
  }

  getNameError(): string {
    if (this.nameControl?.hasError('required')) {
      return 'Nome é obrigatório';
    }
    if (this.nameControl?.hasError('minlength')) {
      return 'Nome deve ter no mínimo 3 caracteres';
    }
    return '';
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

  getConfirmPasswordError(): string {
    if (this.confirmPasswordControl?.hasError('required')) {
      return 'Confirmação de senha é obrigatória';
    }
    if (this.registerForm.hasError('passwordMismatch') && this.confirmPasswordControl?.touched) {
      return 'As senhas não coincidem';
    }
    return '';
  }

  async onSubmit(): Promise<void> {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    try {
      const { name, email, password } = this.registerForm.value;
      await this.authService.register({ username: name, email, password }).toPromise();
      
      this.successMessage = 'Conta criada com sucesso! Redirecionando...';
      
      setTimeout(() => {
        this.router.navigate(['/dashboard']);
      }, 2000);
    } catch (error: any) {
      this.errorMessage = error?.error?.detail || 'Erro ao criar conta. Tente novamente.';
    } finally {
      this.isLoading = false;
    }
  }
}
