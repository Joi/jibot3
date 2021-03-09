import {Entity, PrimaryGeneratedColumn, Column } from "typeorm";
@Entity()
export class Books {
	@PrimaryGeneratedColumn() id: number;
    @Column("varchar", { nullable: false}) title: string;
    @Column("varchar", { nullable: true}) url: string;
    @Column("varchar", { nullable: true}) content: string;
    //@Column() topics: string;
    // @Column() people: string;
    // @Column() places: string;
    // @Column() organizations: string;
    // @Column() nouns: string;
    // @Column() verbs: string;
}