import {Entity, PrimaryGeneratedColumn, Column } from "typeorm";
@Entity()
export class Books {
	@PrimaryGeneratedColumn() id: number;
    @Column("varchar", { nullable: false}) title: string;
    @Column("varchar", { nullable: true}) url: string;
    @Column("varchar", { nullable: true}) content: string;
    @Column("varchar", { nullable: true}) people: string;
    @Column("varchar", { nullable: true}) places: string;
    @Column("varchar", { nullable: true}) organizations: string;
}