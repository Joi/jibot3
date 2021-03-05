import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';

const materialModules = [
	MatButtonModule,
	MatCardModule,
	MatIconModule,
    MatSidenavModule,
	MatTableModule,
    MatToolbarModule
]
@NgModule({
	declarations: [],
	exports: [
		... materialModules
	],
	imports: [
		CommonModule,
		... materialModules
	]
})
export class MaterialModule { }