import { useState } from 'react';
import axios from 'axios';
import useRequest from '../../hooks/use-request';
import { useRouter } from 'next/router';

export default function Signup() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { request, errors } = useRequest({
    url: '/api/users/signup',
    method: 'post', 
    body: { email, password },
    onSuccess: () => {
        setSuccess('Signup successful!');
        setEmail('');
        setPassword('');
        router.push('/auth/signin');
    }   
    });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
        await request();
  };

  return (
    <div className="container mt-5" style={{ maxWidth: 400 }}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email address</label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        {Array.isArray(errors) && errors.length > 0 && (
          <div className="alert alert-danger">
            {errors.map((err, idx) => (
              <div key={idx}>{err.message}</div>
            ))}
          </div>
        )}
        {typeof errors === 'object' && !Array.isArray(errors) && errors?.message && (
          <div className="alert alert-danger">{errors.message}</div>
        )}
        {success && <div className="alert alert-success">{success}</div>}
        <button type="submit" className="btn btn-primary w-100">Sign Up</button>
      </form>
    </div>
  );
}
