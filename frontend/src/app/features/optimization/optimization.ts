import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
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
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.optimizationForm = this.fb.group({
      productName: ['', [Validators.required]],
      costFunction: ['', [Validators.required]],
      demandFunction: ['', [Validators.required]]
    });

    this.loadOptimizations();
  }

  async loadOptimizations(): Promise<void> {
    this.isLoadingList = true;
    try {
      const data = await firstValueFrom(this.optimizationService.listOptimizations());
      this.optimizations = data;
      this.isLoadingList = false;
      this.cdr.detectChanges();
    } catch (error) {
      console.error('Erro ao carregar otimizações:', error);
      this.isLoadingList = false;
      this.cdr.detectChanges();
    }
  }

  async onOptimizationSelect(event: Event): Promise<void> {
    const select = event.target as HTMLSelectElement;
    const value = select.value;

    if (value === 'new') {
      this.selectedOptimizationName = null;
      this.currentResult = null;
      this.optimizationForm.reset();
      this.cdr.detectChanges();
    } else {
      this.selectedOptimizationName = value;
      
      try {
        // Buscar detalhes completos da otimização selecionada
        const result = await firstValueFrom(this.optimizationService.getOptimization(value));
        
        this.optimizationForm.patchValue({
          productName: result.optimization_name,
          costFunction: result.cost_function,
          demandFunction: result.demand_function
        });
        
        this.currentResult = result;
        this.cdr.detectChanges();
        console.log('Produto carregado:', result.optimization_name);
      } catch (error) {
        console.error('Erro ao carregar otimização:', error);
      }
    }
  }

  async onSubmit(): Promise<void> {
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

    try {
      console.log('Processando otimização:', formData.optimization_name);
      
      const request$ = this.selectedOptimizationName
        ? this.optimizationService.updateOptimization(this.selectedOptimizationName, formData)
        : this.optimizationService.makeOptimization(formData);
      
      await firstValueFrom(request$);
      
      // Atualizar selectedOptimizationName se o nome mudou
      this.selectedOptimizationName = formData.optimization_name;
      
      // Recarregar a lista primeiro para garantir que o novo/atualizado item existe
      await this.loadOptimizations();
      
      // Aguardar um pouco para garantir que o backend processou tudo
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Após criar/atualizar, buscar os detalhes completos usando o novo nome
      const detailedResult = await firstValueFrom(
        this.optimizationService.getOptimization(formData.optimization_name)
      );
      
      this.currentResult = detailedResult;
      this.isLoading = false;
      this.cdr.detectChanges();
      console.log('Otimização processada com sucesso');
    } catch (error: any) {
      console.error('Erro ao processar otimização:', error);
      
      // Tratar erro de validação do Pydantic (422)
      if (error?.status === 422 && error?.error?.detail) {
        const details = error.error.detail;
        
        if (Array.isArray(details)) {
          // Extrair apenas as mensagens relevantes, removendo prefixos técnicos
          const messages = details.map((err: any) => {
            let msg = err.msg || '';
            // Remover "Value error, " do início da mensagem se existir
            msg = msg.replace(/^Value error,\s*/i, '');
            return msg;
          }).filter(msg => msg).join('\n');
          
          this.errorMessage = messages || 'Erro de validação nas funções';
        } else if (typeof details === 'string') {
          this.errorMessage = details;
        } else {
          this.errorMessage = 'Erro de validação. Verifique se as funções usam as variáveis corretas (q para custo, p para demanda).';
        }
      } else {
        this.errorMessage = error?.error?.detail || 'Erro ao processar otimização. Verifique as funções inseridas.';
      }
      
      this.isLoading = false;
      this.cdr.detectChanges();
    }
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
