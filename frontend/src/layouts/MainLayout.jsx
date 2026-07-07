import { Outlet, useLocation } from 'react-router-dom'
import Navbar from '../components/Navbar'
import BottomNav from '../components/BottomNav'

export default function MainLayout() {
  const { pathname } = useLocation()

  return (
    <div className="min-h-screen gradient-hero flex flex-col">
      <Navbar />
      <main className="flex-1 pb-20 lg:pb-0 page-enter" key={pathname}>
        <Outlet />
      </main>
      <BottomNav />
    </div>
  )
}
