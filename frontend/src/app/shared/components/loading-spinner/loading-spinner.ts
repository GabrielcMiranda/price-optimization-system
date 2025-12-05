import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

type SpinnerSize = 'sm' | 'md' | 'lg' | 'xl';

@Component({
  selector: 'app-loading-spinner',
  imports: [CommonModule],
  templateUrl: './loading-spinner.html',
  styleUrl: './loading-spinner.scss',
})
export class LoadingSpinner {
  @Input() size: SpinnerSize = 'md';
  @Input() message = '';
  @Input() fullscreen = false;

  get spinnerSizeClasses(): string {
    const sizes = {
      sm: 'h-6 w-6',
      md: 'h-10 w-10',
      lg: 'h-16 w-16',
      xl: 'h-24 w-24'
    };
    return sizes[this.size];
  }

  get containerClasses(): string {
    const baseClasses = 'flex flex-col items-center justify-center';
    const fullscreenClasses = this.fullscreen 
      ? 'fixed inset-0 bg-white bg-opacity-90 z-50' 
      : 'py-8';
    return `${baseClasses} ${fullscreenClasses}`;
  }
}
