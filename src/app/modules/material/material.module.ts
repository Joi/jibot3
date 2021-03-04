import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';

const materialModules = [
	MatButtonModule,
	MatCardModule,
	MatIconModule,
	MatTableModule,
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