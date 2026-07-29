import Link from 'next/link';

export default function Header({ currentUser }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 32px', backgroundColor: '#f8f9fa', borderBottom: '1px solid #eee' }}>
      <h1>My App</h1>
      <div>
        {currentUser ? (
          <>
            <span style={{ marginRight: 16 }}>Welcome, {currentUser.email}!</span>
            <Link href="/auth/signout" legacyBehavior>
              <a style={{ marginRight: 16 }}>Logout</a>
            </Link>
          </>
        ) : (
          <>
            <Link href="/auth/signin" legacyBehavior>
              <a style={{ marginRight: 16 }}>Sign In</a>
            </Link>
            <Link href="/auth/signup" legacyBehavior>
              <a>Sign Up</a>
            </Link>
          </>
        )}
      </div>
    </div>
  );
}