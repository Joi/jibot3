import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import { SidenavService } from './services/sidenav.service';
import { BehaviorSubject } from 'rxjs';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements AfterViewInit {
	@ViewChild('sidenav', { static: false }) sidenav: MatSidenav;
    public title = 'jibot3';
	constructor(
		private router: Router,
		private sidenavService: SidenavService
	) {
		this.router.events.subscribe(this.sidenav?.close);

	}
	ngAfterViewInit() {
		this.sidenavService.toggle.subscribe((doIt:boolean) => (doIt) ? this.sidenav.opened = !this.sidenav.opened : null);
	}
}
