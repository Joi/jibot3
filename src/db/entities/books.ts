import {Entity, PrimaryGeneratedColumn, Column, AfterLoad} from "typeorm";
@Entity()
export class Books {
	@PrimaryGeneratedColumn() id: number;
    @Column() title: string;
    @Column() url: string;
}