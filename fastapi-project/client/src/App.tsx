import { Route, Routes } from 'react-router-dom'
import { Home } from './pages/home'
import { Login } from './pages/login'
import { PostCreatePage } from './pages/post-create'
import { PostDetailPage } from './pages/post-detail'
import { Profile } from './pages/profile'
import { Register } from './pages/register'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/posts/new" element={<PostCreatePage />} />
      <Route path="/posts/:id" element={<PostDetailPage />} />
    </Routes>
  )
}

export default App
