import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card',
  imports: [CommonModule],
  templateUrl: './card.html',
  styleUrl: './card.scss',
})
export class Card {
  @Input() elevated = true;
  @Input() padding = true;
  @Input() hoverable = false;

  get cardClasses(): string {
    const baseClasses = 'bg-white rounded-lg border border-gray-200 transition-all duration-200';
    const shadowClass = this.elevated ? 'shadow-md' : '';
    const paddingClass = this.padding ? 'p-6' : '';
    const hoverClass = this.hoverable ? 'hover:shadow-lg cursor-pointer' : '';

    return `${baseClasses} ${shadowClass} ${paddingClass} ${hoverClass}`;
  }
}
