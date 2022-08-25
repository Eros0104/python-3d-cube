import pygame
import numpy
import math

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

position_x = WIDTH/2
position_y = HEIGHT/2

angle = 0

points = []

points.append(numpy.matrix([-1, -1, 1]))
points.append(numpy.matrix([1, -1, 1]))
points.append(numpy.matrix([1, 1, 1]))
points.append(numpy.matrix([-1, 1, 1]))
points.append(numpy.matrix([-1, -1, -1]))
points.append(numpy.matrix([1, -1, -1]))
points.append(numpy.matrix([1, 1, -1]))
points.append(numpy.matrix([-1, 1, -1]))

projection_matrix = numpy.matrix([
  [1, 0, 0],
  [0, 1, 0]
])

projected_points = [
  [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
  pygame.draw.line(screen, WHITE_COLOR, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()

while True: 
  clock.tick(60)
  for event in pygame.event.get():
    
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  rotation_z = numpy.matrix([
    [math.cos(angle), -math.sin(angle), 0],
    [math.sin(angle), math.cos(angle), 0],
    [0, 0, 1],
  ])

  rotation_y = numpy.matrix([
    [math.cos(angle), 0, math.sin(angle)],
    [0, 1, 0],
    [-math.sin(angle), 0, math.cos(angle)],
  ])

  angle += 0.01
  
  screen.fill(BLACK_COLOR)

  i = 0
  for point in points:
    three_d_point = point.reshape((3,1))
    rotated2d = numpy.dot(rotation_z, three_d_point)
    rotated3d = numpy.dot(rotation_y, rotated2d)
    projected2d = numpy.dot(projection_matrix, rotated3d)

    x = int(projected2d[0][0] * scale) + position_x
    y = int(projected2d[1][0] * scale) + position_y

    projected_points[i] = [x, y]
    pygame.draw.circle(screen, WHITE_COLOR, (x, y), 1)
    i += 1

  # connect_points(0, 1, projected_points)
  # connect_points(1, 2, projected_points)
  # connect_points(2, 3, projected_points)
  # connect_points(3, 0, projected_points)

  # connect_points(4, 5, projected_points)
  # connect_points(5, 6, projected_points)
  # connect_points(6, 7, projected_points)
  # connect_points(7, 4, projected_points)

  # connect_points(0, 4, projected_points)
  # connect_points(1, 5, projected_points)
  # connect_points(2, 6, projected_points)
  # connect_points(3, 7, projected_points)

  for p in range(4):
    connect_points(p, (p + 1) % 4, projected_points)
    connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
    connect_points(p, (p + 4), projected_points)


  pygame.display.update()