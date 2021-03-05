import {Entity, PrimaryGeneratedColumn, Column } from "typeorm";
@Entity()
export class Options {
	@PrimaryGeneratedColumn() id: number;
    @Column() name: string;
    @Column() value: any;
}