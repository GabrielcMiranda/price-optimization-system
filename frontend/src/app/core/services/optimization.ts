import { Injectable } from '@angular/core';
import { ApiService } from './api';
import { 
  OptimizationRequest, 
  OptimizationResponse, 
  StandardOutput 
} from '../models/optimization.model';

@Injectable({
  providedIn: 'root',
})
export class OptimizationService {

  constructor(private api: ApiService) {}
  
  makeOptimization(request: OptimizationRequest) {
    return this.api.post<StandardOutput>('optimizations/', request);
  }

  getOptimization(optimizationName: string) {
    return this.api.get<OptimizationResponse>(`optimizations/${optimizationName}`);
  }

  updateOptimization(optimizationName: string, request: OptimizationRequest) {
    return this.api.put<StandardOutput>(`optimizations/${optimizationName}`, request);
  }

  listOptimizations() {
    return this.api.get<OptimizationRequest[]>('optimizations/');
  }

}
