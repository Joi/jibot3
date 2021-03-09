import {MigrationInterface, QueryRunner, Table} from "typeorm";
export class CreateOptionsTable1615298780304 implements MigrationInterface {
    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(new Table({
            name: "options",
            columns: [
                {
                    name: "id",
                    type: "integer",
                    isPrimary: true,
                    isGenerated: true,
                    generationStrategy: 'increment'
                },
                {
                    name: "name",
                    type: "text",
                    isNullable: false,
                    isUnique: true,
                },
                {
                    name: "value",
                    type: "text",
                }
            ]
        }), true);
    }
    public async down(queryRunner: QueryRunner): Promise<void> {
        return await queryRunner.dropTable("books");
    }

}
