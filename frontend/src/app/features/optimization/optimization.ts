import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { InputComponent } from '../../shared/components/input/input';
import { Button } from '../../shared/components/button/button';
import { Card } from '../../shared/components/card/card';
import { LoadingSpinner } from '../../shared/components/loading-spinner/loading-spinner';
import { OptimizationService } from '../../core/services/optimization';
import { AuthService } from '../../core/services/auth';
import { OptimizationRequest, OptimizationResponse } from '../../core/models/optimization.model';

@Component({
  selector: 'app-optimization',
  imports: [CommonModule, ReactiveFormsModule, InputComponent, Button, Card, LoadingSpinner],
  templateUrl: './optimization.html',
  styleUrl: './optimization.scss',
})
export class Optimization implements OnInit {
  optimizationForm!: FormGroup;
  optimizations: OptimizationRequest[] = [];
  selectedOptimizationName: string | null = null;
  currentResult: OptimizationResponse | null = null;
  isLoading = false;
  isLoadingList = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private optimizationService: OptimizationService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.optimizationForm = this.fb.group({
      productName: ['', [Validators.required]],
      costFunction: ['', [Validators.required]],
      demandFunction: ['', [Validators.required]]
    });

    this.loadOptimizations();
  }

  loadOptimizations(): void {
    this.isLoadingList = true;
    this.optimizationService.listOptimizations().subscribe({
      next: (data) => {
        this.optimizations = data;
        this.isLoadingList = false;
      },
      error: (error) => {
        console.error('Erro ao carregar otimizações:', error);
        this.isLoadingList = false;
      }
    });
  }

  onOptimizationSelect(event: Event): void {
    const select = event.target as HTMLSelectElement;
    const value = select.value;

    if (value === 'new') {
      this.selectedOptimizationName = null;
      this.currentResult = null;
      this.optimizationForm.reset();
    } else {
      this.selectedOptimizationName = value;
      
      // Buscar detalhes completos da otimização selecionada
      this.optimizationService.getOptimization(value).subscribe({
        next: (result) => {
          this.optimizationForm.patchValue({
            productName: result.optimization_name,
            costFunction: result.cost_function,
            demandFunction: result.demand_function
          });
          this.currentResult = result;
        },
        error: (error) => {
          console.error('Erro ao carregar otimização:', error);
        }
      });
    }
  }

  onSubmit(): void {
    if (this.optimizationForm.invalid) {
      this.optimizationForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const formData = {
      optimization_name: this.optimizationForm.value.productName,
      cost_function: this.optimizationForm.value.costFunction,
      demand_function: this.optimizationForm.value.demandFunction
    };

    const request$ = this.selectedOptimizationName
      ? this.optimizationService.updateOptimization(this.selectedOptimizationName, formData)
      : this.optimizationService.makeOptimization(formData);

    request$.subscribe({
      next: (result) => {
        // Após criar/atualizar, buscar os detalhes completos
        this.optimizationService.getOptimization(formData.optimization_name).subscribe({
          next: (detailedResult) => {
            this.currentResult = detailedResult;
            this.isLoading = false;
            this.loadOptimizations();
          },
          error: (error) => {
            console.error('Erro ao buscar detalhes:', error);
            this.isLoading = false;
          }
        });
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail || 'Erro ao processar otimização. Verifique as funções inseridas.';
        this.isLoading = false;
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  get productNameControl() {
    return this.optimizationForm.get('productName');
  }

  get costFunctionControl() {
    return this.optimizationForm.get('costFunction');
  }

  get demandFunctionControl() {
    return this.optimizationForm.get('demandFunction');
  }

  getProductNameError(): string {
    return this.productNameControl?.hasError('required') ? 'Nome do produto é obrigatório' : '';
  }

  getCostFunctionError(): string {
    return this.costFunctionControl?.hasError('required') ? 'Função de custo é obrigatória' : '';
  }

  getDemandFunctionError(): string {
    return this.demandFunctionControl?.hasError('required') ? 'Função de demanda é obrigatória' : '';
  }
}
