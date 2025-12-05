import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
})
export class Navbar {
  @Input() userName = '';
  @Input() showSidebarToggle = false;
  @Output() sidebarToggled = new EventEmitter<void>();
  @Output() logout = new EventEmitter<void>();

  showUserMenu = false;

  toggleSidebar(): void {
    this.sidebarToggled.emit();
  }

  toggleUserMenu(): void {
    this.showUserMenu = !this.showUserMenu;
  }

  onLogout(): void {
    this.showUserMenu = false;
    this.logout.emit();
  }
}
