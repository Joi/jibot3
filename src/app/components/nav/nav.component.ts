import { Component, OnInit } from '@angular/core';
import { routes } from '@app/app-routing.module';
@Component({
    selector: 'app-nav',
    templateUrl: './nav.component.html',
    styleUrls: ['./nav.component.scss']
})
export class NavComponent implements OnInit {
    constructor() { 
        console.log(routes);
    }

    ngOnInit(): void {
        
    }

}
