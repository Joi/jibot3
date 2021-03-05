import { Component, ViewChild } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
	@ViewChild('sidenav', { static: false }) sidenav: MatSidenav;
    public title = 'jibot3';
    constructor(
		private router: Router,
	) {
		this.router.events.subscribe(this.sidenav?.close);
	}
}
