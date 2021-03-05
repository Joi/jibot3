import {MigrationInterface, QueryRunner, Table} from "typeorm";

export class CreateBookTable1614880942662 implements MigrationInterface {
    public async up(queryRunner: QueryRunner): Promise<void> {
        return await queryRunner.createTable(new Table({
            name: "books",
            columns: [
                {
                    name: "id",
                    type: "integer",
                    isPrimary: true,
                    isGenerated: true,
                    generationStrategy: 'increment'
                },
                {
                    name: "title",
                    type: "varchar",
                    isNullable: false,
                },
                {
                    name: "url",
                    type: "text",
                    isNullable: false
                },
            ]
        }), true);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        return await queryRunner.dropTable("books");
    }

}
