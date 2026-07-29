import {scrypt,randomBytes} from 'crypto';
import { promisify } from 'util';

const scryptAsync = promisify(scrypt);

export class PasswordHashing {

    static async toHash(password: string): Promise<string> {
        // Implement your hashing logic here, e.g., using bcrypt
        const salt = randomBytes(8).toString('hex');

        const buf= (await scryptAsync(password, salt, 64)) as Buffer;
        // For demonstration purposes, we'll just return the password as is (not secure)
        return `${buf.toString('hex')}.${salt}`; // Replace with actual hashing logic
    }

    static async compare(storedPassword: string, suppliedPassword: string): Promise<boolean> {
        const [hashedPassword, salt] = storedPassword.split('.');
        const buf = await scryptAsync(suppliedPassword, salt, 64) as Buffer;
        return buf.toString('hex') === hashedPassword; // Replace with actual comparison logic
    }
}