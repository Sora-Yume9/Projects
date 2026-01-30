import pygame
import numpy as np
from assets import squ as squ
from assets import opp_squ as opp_squ
import random
import torch
pygame.init()
display = [1000, 600]
screen = pygame.display.set_mode(display)
clock = pygame.time.Clock()

# timing
last_action_time = 0
action_interval = 12000  # ms between generations
prediction_interval_ms = 50
last_prediction_time = 0

generation = 0
speed = 10
gravity = 1.2          # pixels / frame^2
jump_strength = -18.0  # initial vy when jumping (negative = up)

mutation_rate = 0.05
mutation_strength = 0.05

num_players = 6
players = []
opponents = []


# create agents
for _ in range(num_players):
    x = 50.0 + random.randint(10, 50)
    y = 500.0 + random.randint(10, 100)
    players.append(squ(x, y, [0,0,255]))

for _ in range(num_players):
    x = 900.0 + random.randint(10, 50)
    y = 500.0 + random.randint(10, 100)
    opponents.append(opp_squ(x, y, [255,0,0]))

running = True

# utility: find nearest opponent for a given player
def nearest_agent(source, targets):
    best = None
    best_dist = float('inf')
    best_dx = 0.0
    best_dy = 0.0
    best_opp_vy = 0.0
    opp_x,opp_y = 0,0
    for t in targets:
        if not t.is_alive:
            continue
        dx = source.x - t.x
        dy = source.y - t.y
        d = np.hypot(dx, dy)
        if d < best_dist:
            best_dist = d
            best = t
            best_dx = dx
            best_dy = dy
            opp_x = t.x
            opp_y = t.y
            best_opp_vy = t.vy
    return best, best_dx, best_dy, best_dist, best_opp_vy,opp_x,opp_y

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- walls ----
    left_wall = pygame.Rect(0, 0, 5, display[1])
    right_wall = pygame.Rect(display[0] - 5, 0, 5, display[1])
    top_wall = pygame.Rect(0, 0, display[0], 5)
    bottom_wall = pygame.Rect(0, display[1] - 6, display[0], 6)

    screen.fill((0,0,0))

    # -- compute nearest enemies and update dx/dy/distance for inputs --
    for p in players:
        if not p.is_alive:
            continue
        nearest_o, dx, dy, dist,opp_vy,opp_x,opp_y = nearest_agent(p, opponents)
        if nearest_o is not None:
            p.dx = dx
            p.dy = dy
            p.opp_vy=opp_vy
            p.opp_x=opp_x
            p.opp_y=opp_y
            p.distance = dist
        else:
            # no alive opponents
            p.dx = 0.0
            p.dy = 0.0
            p.opp_x=opp_x
            p.opp_y=opp_y
            p.opp_vy=opp_vy
            p.distance = float('inf')

    for o in opponents:
        if not o.is_alive:
            continue
        nearest_p, dx, dy, dist,opp_vy,opp_x,opp_y = nearest_agent(o, players)
        if nearest_p is not None:
            # note: for opponent we may want vector towards players; keep sign consistent with your earlier code
            o.dx = -dx
            o.dy = -dy
            o.opp_x=opp_x
            o.opp_y=opp_y
            o.opp_vy=opp_vy
            o.distance = dist
        else:
            o.dx = 0.0
            o.dy = 0.0
            o.opp_x=opp_x
            o.opp_y=opp_y
            o.opp_vy=opp_vy
            o.distance = float('inf')

        for p in players:
            if p.is_alive:
                nearest_o, dx, dy, dist, opp_vy, opp_x, opp_y = nearest_agent(p, opponents)
                p.fitness += dist * 0.5          # alive & far from chaser
            else:
                p.fitness -= 100

    

    runner = max(players, key=lambda a: getattr(a, 'fitness', -float('inf')))
    chaser = min(opponents, key=lambda a: getattr(a, 'distance', float('inf')))


    # --- physics, prediction, drawing ---
    do_predict = (current_time - last_prediction_time) >= prediction_interval_ms
    if do_predict:
        last_prediction_time = current_time

    for agent in players + opponents:
        if not agent.is_alive:
            continue

        # physics
        if not hasattr(agent, 'vy'):
            agent.vy = 0.0
        agent.vy += gravity
        agent.y += agent.vy

        # temporary rect for collision / wall handling
        player_rect = pygame.Rect(int(agent.x), int(agent.y), agent.width, agent.height)

        # floor collision
        if player_rect.bottom >= bottom_wall.top:
            player_rect.bottom = bottom_wall.top
            agent.vy = 0.0
            agent.on_ground = True
        else:
            agent.on_ground = False

        # left/right wall collisions (clamp x)
        if player_rect.left < left_wall.right:
            player_rect.left = left_wall.right
        elif player_rect.right > right_wall.left:
            player_rect.right = right_wall.left

        # update agent position from rect
        agent.x = float(player_rect.x)
        agent.y = float(player_rect.y)

        # draw agent
        pygame.draw.rect(screen, agent.color, player_rect)

        # predict (only on interval)
        if do_predict:
            # build input: normalized coordinates + on_ground + vertical speed
            dx = getattr(agent, 'dx', 0.0)
            dy = getattr(agent, 'dy', 0.0)
            distance = getattr(agent, 'distance', display[0])
            inp = np.array([[agent.x/display[0],
                             agent.y/display[1],
                             dx/display[0],
                             dy/display[1],
                             agent.opp_x/display[0],
                             agent.opp_y/display[1],
                             agent.opp_vy/50.0,
                             1.0 if getattr(agent, 'on_ground', False) else 0.0,
                             (agent.vy/50.0)]], dtype=np.float32)

            try:
                inp = torch.tensor(inp).float()
                pred = agent.model(inp)[0]
            except Exception:
                inp = torch.tensor(inp).float()
                pred = agent.model(inp)[0]

            # actions
            if pred[0] >= 0.5 and getattr(agent, 'on_ground', False):
                agent.vy = jump_strength
            if pred[1] >= 0.5:
                agent.x -= speed
            if pred[2] >= 0.5:
                agent.x += speed

    # --- collisions between players and opponents (check all alive pairs) ---
    for p in players:
        if not p.is_alive:
            continue
        rect_p = pygame.Rect(int(p.x), int(p.y), p.width, p.height)
        for o in opponents:
            if not o.is_alive:
                continue
            rect_o = pygame.Rect(int(o.x), int(o.y), o.width, o.height)
            if rect_p.colliderect(rect_o):
                p.is_alive = False
               
                # optional: record fitness/time-alive etc.

    # --- evolution / mutation / respawn ---
    if current_time - last_action_time >= action_interval or all(not p.is_alive for p in players):
        # choose weights from runner/chaser (they were selected earlier from alive lists)
        runner_weights = list(runner.model.parameters())
        chaser_weights = list(chaser.model.parameters())


        # mutate and copy runner to all players
        for run in players:
            with torch.no_grad():
                for w_src, w_dst in zip(runner_weights, run.model.parameters()):
                    # generate mutation noise
                    noise = torch.randn_like(w_src) * mutation_strength
                    mask  = (torch.rand_like(w_src) < mutation_rate)

                    # apply mutation
                    mutated = w_src + noise * mask

                    # copy into destination model
                    w_dst.copy_(mutated)


        # mutate and copy chaser to all opponents
        for chase in opponents:
            with torch.no_grad():
                for w_src, w_dst in zip(chaser_weights, chase.model.parameters()):
                    # generate mutation noise
                    noise = torch.randn_like(w_src) * mutation_strength
                    mask  = (torch.rand_like(w_src) < mutation_rate)

                    # apply mutation
                    mutated = w_src + noise * mask

                    # copy into destination model
                    w_dst.copy_(mutated)

        # respawn all agents
        for re in players:
            re.x = 50.0 + random.randint(1,50)
            re.y = 500.0 + random.randint(1,20)
            re.is_alive = True
            re.vy = 0.0
            re.on_ground = True
            re.distance = float('inf')
        for opp_re in opponents:
            opp_re.x = 900.0 + random.randint(1,50)
            opp_re.y = 500.0 + random.randint(1,20)
            opp_re.is_alive = True
            opp_re.vy = 0.0
            opp_re.on_ground = True
            opp_re.distance = float('inf')
        for p in players:
            p.fitness *= 0.9  # keep some memory, but allow evolution to adapt

        generation += 1
        print("Generation:", generation)
        last_action_time = current_time

    # draw walls
    pygame.draw.rect(screen, (255,255,255), left_wall)
    pygame.draw.rect(screen, (255,255,255), right_wall)
    pygame.draw.rect(screen, (255,255,255), top_wall)
    pygame.draw.rect(screen, (255,255,255), bottom_wall)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
