import {Entity, PrimaryGeneratedColumn, Column, AfterLoad} from "typeorm";
@Entity()
export class Book {
    @PrimaryGeneratedColumn() id: number;
    @Column() title: string;
    @Column() url: string;
}