import { useState } from 'react';
import Router from 'next/router';
import useRequest from '../../hooks/use-request';

const Signin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { request, errors } = useRequest({
    url: '/api/users/signin',
    method: 'post',
    body: {
      email, password
    },
    onSuccess: () => Router.push('/')
  });

  const onSubmit = async (event) => {
    event.preventDefault();
    await request();
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <form onSubmit={onSubmit} style={{ minWidth: 320, maxWidth: 400, width: '100%', padding: 32, border: '1px solid #eee', borderRadius: 8, background: '#fff', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
        <h1 style={{ textAlign: 'center', marginBottom: 24 }}>Sign In</h1>
        <div className="form-group">
          <label>Email Address</label>
          <input
            value={email}
            onChange={e => setEmail(e.target.value)}
            type="email"
            className="form-control"
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            value={password}
            onChange={e => setPassword(e.target.value)}
            type="password"
            className="form-control"
          />
        </div>
        {Array.isArray(errors) && errors.length > 0 && (
          <div className="alert alert-danger" style={{ marginTop: 16 }}>
            {errors.map((err, idx) => (
              <div key={idx}>{err.message}</div>
            ))}
          </div>
        )}
        {typeof errors === 'object' && !Array.isArray(errors) && errors?.message && (
          <div className="alert alert-danger" style={{ marginTop: 16 }}>{errors.message}</div>
        )}
        <button className="btn btn-primary" style={{ width: '100%', marginTop: 16 }}>Sign In</button>
      </form>
    </div>
  );
};

export default Signin;
