import { useRef, useEffect, useState, useCallback } from 'react'
import * as THREE from 'three'
import styles from './ThreeTerrain.module.css'

export default function ThreeTerrain({ onError }) {
  const canvasRef = useRef(null)
  const containerRef = useRef(null)
  const [webglError, setWebglError] = useState(false)
  const [reducedMotion, setReducedMotion] = useState(false)
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 })

  const triggerError = useCallback(() => {
    setWebglError(true)
    onError?.()
  }, [onError])

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setReducedMotion(mediaQuery.matches)
    const handler = (e) => setReducedMotion(e.matches)
    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }, [])

  // Track container size for proper canvas sizing
  useEffect(() => {
    if (!containerRef.current) return
    
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect
        if (width > 0 && height > 0) {
          setContainerSize({ width, height })
        }
      }
    })
    
    resizeObserver.observe(containerRef.current)
    return () => resizeObserver.disconnect()
  }, [])

  useEffect(() => {
    if (webglError || reducedMotion) return
    if (containerSize.width === 0 || containerSize.height === 0) return

    const canvas = canvasRef.current
    if (!canvas) return

    let renderer, scene, camera, terrain, fieldLines, animationId
    let mouseX = 0, mouseY = 0
    let targetX = 0, targetY = 0

    try {
      renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      })
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
      renderer.setSize(containerSize.width, containerSize.height)
      renderer.setClearColor(0x000000, 0)

      scene = new THREE.Scene()

      const aspect = containerSize.width / containerSize.height
      const frustumSize = 12
      camera = new THREE.OrthographicCamera(
        frustumSize * aspect / -2,
        frustumSize * aspect / 2,
        frustumSize / 2,
        frustumSize / -2,
        0.1,
        100
      )
      camera.position.set(8, 14, 8)
      camera.lookAt(0, 0, 0)

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
      scene.add(ambientLight)

      const dirLight = new THREE.DirectionalLight(0xffffff, 0.8)
      dirLight.position.set(10, 20, 10)
      scene.add(dirLight)

      const fillLight = new THREE.DirectionalLight(0xf5f5f3, 0.3)
      fillLight.position.set(-10, 10, -10)
      scene.add(fillLight)

      const terrainGeometry = createTerrainGeometry()
      const terrainMaterial = new THREE.MeshStandardMaterial({
        color: 0xf5f5f3,
        roughness: 0.95,
        metalness: 0,
        flatShading: true,
      })
      terrain = new THREE.Mesh(terrainGeometry, terrainMaterial)
      terrain.rotation.x = -Math.PI / 2
      scene.add(terrain)

      fieldLines = createFieldLines()
      scene.add(fieldLines)

      const accentGeometry = createAccentElements()
      const accentMaterial = new THREE.MeshBasicMaterial({
        color: 0x2c4a1e,
        transparent: true,
        opacity: 0.6,
      })
      const accents = new THREE.Mesh(accentGeometry, accentMaterial)
      accents.rotation.x = -Math.PI / 2
      scene.add(accents)

      const handleResize = () => {
        if (!renderer || !camera || !containerRef.current) return
        const width = containerRef.current.clientWidth
        const height = containerRef.current.clientHeight
        if (width === 0 || height === 0) return
        
        const newAspect = width / height
        const frustumSize = 12
        camera.left = frustumSize * newAspect / -2
        camera.right = frustumSize * newAspect / 2
        camera.top = frustumSize / 2
        camera.bottom = frustumSize / -2
        camera.updateProjectionMatrix()
        renderer.setSize(width, height)
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
      }

      const handleMouseMove = (e) => {
        if (reducedMotion) return
        const rect = canvas.getBoundingClientRect()
        if (rect.width === 0 || rect.height === 0) return
        mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1
        mouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1
      }

      canvas.addEventListener('mousemove', handleMouseMove)
      window.addEventListener('resize', handleResize)

      const animate = () => {
        animationId = requestAnimationFrame(animate)

        if (!reducedMotion) {
          targetX = mouseX * 0.8
          targetY = mouseY * 0.5

          camera.position.x += (targetX - camera.position.x) * 0.02
          camera.position.z += (targetY - camera.position.z) * 0.02
          camera.lookAt(0, 0, 0)

          const time = performance.now() * 0.0003
          terrain.rotation.z = Math.sin(time) * 0.008
          fieldLines.rotation.z = Math.sin(time) * 0.008
          accents.rotation.z = Math.sin(time) * 0.008
        }

        renderer.render(scene, camera)
      }

      animate()

      return () => {
        cancelAnimationFrame(animationId)
        canvas.removeEventListener('mousemove', handleMouseMove)
        window.removeEventListener('resize', handleResize)
        if (terrainGeometry) terrainGeometry.dispose()
        if (terrainMaterial) terrainMaterial.dispose()
        if (fieldLines) fieldLines.geometry.dispose()
        if (fieldLines.material) fieldLines.material.dispose()
        if (accentGeometry) accentGeometry.dispose()
        if (accentMaterial) accentMaterial.dispose()
        renderer.dispose()
      }
    } catch (err) {
      console.warn('Three.js initialization failed, falling back to SVG:', err)
      triggerError()
    }
  }, [webglError, reducedMotion, triggerError, containerSize])

  if (webglError || reducedMotion) {
    return null
  }

  return (
    <div ref={containerRef} className={styles.container}>
      <canvas ref={canvasRef} className={styles.canvas} aria-hidden="true" />
    </div>
  )
}

function createTerrainGeometry() {
  const width = 14
  const depth = 14
  const segments = 28

  const geometry = new THREE.PlaneGeometry(width, depth, segments, segments)
  const positions = geometry.attributes.position
  const count = positions.count

  function noise(x, z) {
    const n = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453
    return (n - Math.floor(n)) * 2 - 1
  }

  for (let i = 0; i < count; i++) {
    const x = positions.getX(i)
    const z = positions.getY(i)

    const distFromCenter = Math.sqrt(x * x + z * z)
    const edgeFalloff = Math.max(0, 1 - distFromCenter / 8)

    let height = 0

    height += noise(x * 0.4, z * 0.4) * 0.35
    height += noise(x * 0.8, z * 0.8) * 0.15
    height += noise(x * 1.6, z * 1.6) * 0.06

    height *= edgeFalloff

    if (distFromCenter > 6.5) {
      height *= Math.max(0, (7.5 - distFromCenter) / 1)
    }

    positions.setZ(i, height)
  }

  geometry.computeVertexNormals()
  return geometry
}

function createFieldLines() {
  const linesGeometry = new THREE.BufferGeometry()
  const positions = []
  const colors = []

  const fieldCount = 5
  const fieldSize = 14 / fieldCount
  const lineColor = new THREE.Color(0x0a0a0a)
  const lineOpacity = 0.08

  for (let i = 0; i <= fieldCount; i++) {
    const pos = -7 + i * fieldSize

    positions.push(-7, 0.02, pos, 7, 0.02, pos)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity)

    positions.push(pos, 0.02, -7, pos, 0.02, 7)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity)
  }

  for (let i = 1; i < fieldCount; i++) {
    if (i % 2 === 0) continue
    const pos = -7 + i * fieldSize
    const offset = (Math.sin(i * 2.3) * 0.5)

    positions.push(-7 + offset, 0.025, pos, 7 + offset, 0.025, pos)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity * 0.5)
    colors.push(lineColor.r, lineColor.g, lineColor.b, lineOpacity * 0.5)
  }

  linesGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
  linesGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 4))

  const material = new THREE.LineBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 1,
  })

  return new THREE.LineSegments(linesGeometry, material)
}

function createAccentElements() {
  const geometry = new THREE.BufferGeometry()
  const positions = []
  const indices = []
  let vertexIndex = 0

  const markerPositions = [
    [-4.5, -2.5], [-1.5, 1.5], [2.5, -0.5],
    [4.5, 3.5], [-3.5, 3.5], [0.5, -4.5],
  ]

  markerPositions.forEach(([x, z]) => {
    const size = 0.15 + Math.random() * 0.1
    const height = 0.05

    positions.push(
      x - size, height, z - size,
      x + size, height, z - size,
      x + size, height, z + size,
      x - size, height, z + size,
    )

    indices.push(
      vertexIndex, vertexIndex + 1, vertexIndex + 2,
      vertexIndex, vertexIndex + 2, vertexIndex + 3,
    )
    vertexIndex += 4
  })

  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
  geometry.setIndex(indices)
  geometry.computeVertexNormals()

  return geometry
}