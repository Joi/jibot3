import { Component, OnInit } from '@angular/core';
import { SidenavService } from '@app/services/sidenav.service';
@Component({
	selector: 'app-header',
	templateUrl: './header.component.html',
	styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
	constructor(
		private sidenavService: SidenavService
	) { }
	ngOnInit(): void {	}
	public toggleSidenav = () => this.sidenavService.toggle.next(true);
}
