# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_UTTT')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_UTTT')
    _UTTT = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_UTTT', [dirname(__file__)])
        except ImportError:
            import _UTTT
            return _UTTT
        try:
            _mod = imp.load_module('_UTTT', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _UTTT = swig_import_helper()
    del swig_import_helper
else:
    import _UTTT
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

BOARDSIZE = _UTTT.BOARDSIZE
GRIDSIZE = _UTTT.GRIDSIZE
MAX_THREADS = _UTTT.MAX_THREADS
ANYBOARD = _UTTT.ANYBOARD
X_VAL = _UTTT.X_VAL
O_VAL = _UTTT.O_VAL
OPEN_VAL = _UTTT.OPEN_VAL
STALEMATE = _UTTT.STALEMATE
GAME_WON = _UTTT.GAME_WON
NO_WIN = _UTTT.NO_WIN
ROW_DIMENSION = _UTTT.ROW_DIMENSION
COL_DIMENSION = _UTTT.COL_DIMENSION
VICTORY_VALUE = _UTTT.VICTORY_VALUE
MAX_MOVES = _UTTT.MAX_MOVES
BOARD_VALUE = _UTTT.BOARD_VALUE
GRID_VALUE = _UTTT.GRID_VALUE
PLAYABLE_VALUE = _UTTT.PLAYABLE_VALUE
STATESIZE = _UTTT.STATESIZE
class CGameState(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CGameState, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CGameState, name)
    __repr__ = _swig_repr
    __swig_setmethods__["board"] = _UTTT.CGameState_board_set
    __swig_getmethods__["board"] = _UTTT.CGameState_board_get
    if _newclass:
        board = _swig_property(_UTTT.CGameState_board_get, _UTTT.CGameState_board_set)
    __swig_setmethods__["boardsWon"] = _UTTT.CGameState_boardsWon_set
    __swig_getmethods__["boardsWon"] = _UTTT.CGameState_boardsWon_get
    if _newclass:
        boardsWon = _swig_property(_UTTT.CGameState_boardsWon_get, _UTTT.CGameState_boardsWon_set)
    __swig_setmethods__["currentBoard"] = _UTTT.CGameState_currentBoard_set
    __swig_getmethods__["currentBoard"] = _UTTT.CGameState_currentBoard_get
    if _newclass:
        currentBoard = _swig_property(_UTTT.CGameState_currentBoard_get, _UTTT.CGameState_currentBoard_set)
    __swig_setmethods__["currentTurn"] = _UTTT.CGameState_currentTurn_set
    __swig_getmethods__["currentTurn"] = _UTTT.CGameState_currentTurn_get
    if _newclass:
        currentTurn = _swig_property(_UTTT.CGameState_currentTurn_get, _UTTT.CGameState_currentTurn_set)
    __swig_setmethods__["gameWon"] = _UTTT.CGameState_gameWon_set
    __swig_getmethods__["gameWon"] = _UTTT.CGameState_gameWon_get
    if _newclass:
        gameWon = _swig_property(_UTTT.CGameState_gameWon_get, _UTTT.CGameState_gameWon_set)

    def __init__(self):
        this = _UTTT.new_CGameState()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_CGameState
    __del__ = lambda self: None
CGameState_swigregister = _UTTT.CGameState_swigregister
CGameState_swigregister(CGameState)

class Coord(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Coord, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Coord, name)
    __repr__ = _swig_repr
    __swig_setmethods__["board"] = _UTTT.Coord_board_set
    __swig_getmethods__["board"] = _UTTT.Coord_board_get
    if _newclass:
        board = _swig_property(_UTTT.Coord_board_get, _UTTT.Coord_board_set)
    __swig_setmethods__["row"] = _UTTT.Coord_row_set
    __swig_getmethods__["row"] = _UTTT.Coord_row_get
    if _newclass:
        row = _swig_property(_UTTT.Coord_row_get, _UTTT.Coord_row_set)
    __swig_setmethods__["column"] = _UTTT.Coord_column_set
    __swig_getmethods__["column"] = _UTTT.Coord_column_get
    if _newclass:
        column = _swig_property(_UTTT.Coord_column_get, _UTTT.Coord_column_set)

    def __init__(self):
        this = _UTTT.new_Coord()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_Coord
    __del__ = lambda self: None
Coord_swigregister = _UTTT.Coord_swigregister
Coord_swigregister(Coord)

class MoveList(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MoveList, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MoveList, name)
    __repr__ = _swig_repr
    __swig_setmethods__["length"] = _UTTT.MoveList_length_set
    __swig_getmethods__["length"] = _UTTT.MoveList_length_get
    if _newclass:
        length = _swig_property(_UTTT.MoveList_length_get, _UTTT.MoveList_length_set)
    __swig_setmethods__["moves"] = _UTTT.MoveList_moves_set
    __swig_getmethods__["moves"] = _UTTT.MoveList_moves_get
    if _newclass:
        moves = _swig_property(_UTTT.MoveList_moves_get, _UTTT.MoveList_moves_set)

    def __init__(self):
        this = _UTTT.new_MoveList()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_MoveList
    __del__ = lambda self: None
MoveList_swigregister = _UTTT.MoveList_swigregister
MoveList_swigregister(MoveList)

class Args(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Args, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Args, name)
    __repr__ = _swig_repr
    __swig_setmethods__["layers"] = _UTTT.Args_layers_set
    __swig_getmethods__["layers"] = _UTTT.Args_layers_get
    if _newclass:
        layers = _swig_property(_UTTT.Args_layers_get, _UTTT.Args_layers_set)
    __swig_setmethods__["coords"] = _UTTT.Args_coords_set
    __swig_getmethods__["coords"] = _UTTT.Args_coords_get
    if _newclass:
        coords = _swig_property(_UTTT.Args_coords_get, _UTTT.Args_coords_set)

    def __init__(self):
        this = _UTTT.new_Args()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_Args
    __del__ = lambda self: None
Args_swigregister = _UTTT.Args_swigregister
Args_swigregister(Args)

class HeuristicVal(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, HeuristicVal, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, HeuristicVal, name)
    __repr__ = _swig_repr
    __swig_setmethods__["boardVal"] = _UTTT.HeuristicVal_boardVal_set
    __swig_getmethods__["boardVal"] = _UTTT.HeuristicVal_boardVal_get
    if _newclass:
        boardVal = _swig_property(_UTTT.HeuristicVal_boardVal_get, _UTTT.HeuristicVal_boardVal_set)
    __swig_setmethods__["gridVal"] = _UTTT.HeuristicVal_gridVal_set
    __swig_getmethods__["gridVal"] = _UTTT.HeuristicVal_gridVal_get
    if _newclass:
        gridVal = _swig_property(_UTTT.HeuristicVal_gridVal_get, _UTTT.HeuristicVal_gridVal_set)
    __swig_setmethods__["playableVal"] = _UTTT.HeuristicVal_playableVal_set
    __swig_getmethods__["playableVal"] = _UTTT.HeuristicVal_playableVal_get
    if _newclass:
        playableVal = _swig_property(_UTTT.HeuristicVal_playableVal_get, _UTTT.HeuristicVal_playableVal_set)
    __swig_setmethods__["maxRuns"] = _UTTT.HeuristicVal_maxRuns_set
    __swig_getmethods__["maxRuns"] = _UTTT.HeuristicVal_maxRuns_get
    if _newclass:
        maxRuns = _swig_property(_UTTT.HeuristicVal_maxRuns_get, _UTTT.HeuristicVal_maxRuns_set)
    __swig_setmethods__["index"] = _UTTT.HeuristicVal_index_set
    __swig_getmethods__["index"] = _UTTT.HeuristicVal_index_get
    if _newclass:
        index = _swig_property(_UTTT.HeuristicVal_index_get, _UTTT.HeuristicVal_index_set)
    __swig_setmethods__["montePolicy"] = _UTTT.HeuristicVal_montePolicy_set
    __swig_getmethods__["montePolicy"] = _UTTT.HeuristicVal_montePolicy_get
    if _newclass:
        montePolicy = _swig_property(_UTTT.HeuristicVal_montePolicy_get, _UTTT.HeuristicVal_montePolicy_set)
    __swig_setmethods__["threads"] = _UTTT.HeuristicVal_threads_set
    __swig_getmethods__["threads"] = _UTTT.HeuristicVal_threads_get
    if _newclass:
        threads = _swig_property(_UTTT.HeuristicVal_threads_get, _UTTT.HeuristicVal_threads_set)

    def __init__(self):
        this = _UTTT.new_HeuristicVal()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_HeuristicVal
    __del__ = lambda self: None
HeuristicVal_swigregister = _UTTT.HeuristicVal_swigregister
HeuristicVal_swigregister(HeuristicVal)

class MCHuerArg(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MCHuerArg, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MCHuerArg, name)
    __repr__ = _swig_repr
    __swig_setmethods__["game"] = _UTTT.MCHuerArg_game_set
    __swig_getmethods__["game"] = _UTTT.MCHuerArg_game_get
    if _newclass:
        game = _swig_property(_UTTT.MCHuerArg_game_get, _UTTT.MCHuerArg_game_set)
    __swig_setmethods__["maxRuns"] = _UTTT.MCHuerArg_maxRuns_set
    __swig_getmethods__["maxRuns"] = _UTTT.MCHuerArg_maxRuns_get
    if _newclass:
        maxRuns = _swig_property(_UTTT.MCHuerArg_maxRuns_get, _UTTT.MCHuerArg_maxRuns_set)
    __swig_setmethods__["montePolicy"] = _UTTT.MCHuerArg_montePolicy_set
    __swig_getmethods__["montePolicy"] = _UTTT.MCHuerArg_montePolicy_get
    if _newclass:
        montePolicy = _swig_property(_UTTT.MCHuerArg_montePolicy_get, _UTTT.MCHuerArg_montePolicy_set)
    __swig_setmethods__["seed"] = _UTTT.MCHuerArg_seed_set
    __swig_getmethods__["seed"] = _UTTT.MCHuerArg_seed_get
    if _newclass:
        seed = _swig_property(_UTTT.MCHuerArg_seed_get, _UTTT.MCHuerArg_seed_set)
    __swig_setmethods__["eval"] = _UTTT.MCHuerArg_eval_set
    __swig_getmethods__["eval"] = _UTTT.MCHuerArg_eval_get
    if _newclass:
        eval = _swig_property(_UTTT.MCHuerArg_eval_get, _UTTT.MCHuerArg_eval_set)

    def __init__(self):
        this = _UTTT.new_MCHuerArg()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_MCHuerArg
    __del__ = lambda self: None
MCHuerArg_swigregister = _UTTT.MCHuerArg_swigregister
MCHuerArg_swigregister(MCHuerArg)

class MCST_Args(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MCST_Args, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MCST_Args, name)
    __repr__ = _swig_repr
    __swig_setmethods__["rollout"] = _UTTT.MCST_Args_rollout_set
    __swig_getmethods__["rollout"] = _UTTT.MCST_Args_rollout_get
    if _newclass:
        rollout = _swig_property(_UTTT.MCST_Args_rollout_get, _UTTT.MCST_Args_rollout_set)
    __swig_setmethods__["maxRuns"] = _UTTT.MCST_Args_maxRuns_set
    __swig_getmethods__["maxRuns"] = _UTTT.MCST_Args_maxRuns_get
    if _newclass:
        maxRuns = _swig_property(_UTTT.MCST_Args_maxRuns_get, _UTTT.MCST_Args_maxRuns_set)
    __swig_setmethods__["c"] = _UTTT.MCST_Args_c_set
    __swig_getmethods__["c"] = _UTTT.MCST_Args_c_get
    if _newclass:
        c = _swig_property(_UTTT.MCST_Args_c_get, _UTTT.MCST_Args_c_set)
    __swig_setmethods__["threads"] = _UTTT.MCST_Args_threads_set
    __swig_getmethods__["threads"] = _UTTT.MCST_Args_threads_get
    if _newclass:
        threads = _swig_property(_UTTT.MCST_Args_threads_get, _UTTT.MCST_Args_threads_set)
    __swig_setmethods__["shuffle"] = _UTTT.MCST_Args_shuffle_set
    __swig_getmethods__["shuffle"] = _UTTT.MCST_Args_shuffle_get
    if _newclass:
        shuffle = _swig_property(_UTTT.MCST_Args_shuffle_get, _UTTT.MCST_Args_shuffle_set)
    __swig_setmethods__["bias"] = _UTTT.MCST_Args_bias_set
    __swig_getmethods__["bias"] = _UTTT.MCST_Args_bias_get
    if _newclass:
        bias = _swig_property(_UTTT.MCST_Args_bias_get, _UTTT.MCST_Args_bias_set)
    __swig_setmethods__["scale"] = _UTTT.MCST_Args_scale_set
    __swig_getmethods__["scale"] = _UTTT.MCST_Args_scale_get
    if _newclass:
        scale = _swig_property(_UTTT.MCST_Args_scale_get, _UTTT.MCST_Args_scale_set)
    __swig_setmethods__["bias_multiplier"] = _UTTT.MCST_Args_bias_multiplier_set
    __swig_getmethods__["bias_multiplier"] = _UTTT.MCST_Args_bias_multiplier_get
    if _newclass:
        bias_multiplier = _swig_property(_UTTT.MCST_Args_bias_multiplier_get, _UTTT.MCST_Args_bias_multiplier_set)

    def __init__(self):
        this = _UTTT.new_MCST_Args()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_MCST_Args
    __del__ = lambda self: None
MCST_Args_swigregister = _UTTT.MCST_Args_swigregister
MCST_Args_swigregister(MCST_Args)

class MonteCarloNode(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MonteCarloNode, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MonteCarloNode, name)
    __repr__ = _swig_repr
    __swig_setmethods__["game"] = _UTTT.MonteCarloNode_game_set
    __swig_getmethods__["game"] = _UTTT.MonteCarloNode_game_get
    if _newclass:
        game = _swig_property(_UTTT.MonteCarloNode_game_get, _UTTT.MonteCarloNode_game_set)
    __swig_setmethods__["parent"] = _UTTT.MonteCarloNode_parent_set
    __swig_getmethods__["parent"] = _UTTT.MonteCarloNode_parent_get
    if _newclass:
        parent = _swig_property(_UTTT.MonteCarloNode_parent_get, _UTTT.MonteCarloNode_parent_set)
    __swig_setmethods__["possibleMoves"] = _UTTT.MonteCarloNode_possibleMoves_set
    __swig_getmethods__["possibleMoves"] = _UTTT.MonteCarloNode_possibleMoves_get
    if _newclass:
        possibleMoves = _swig_property(_UTTT.MonteCarloNode_possibleMoves_get, _UTTT.MonteCarloNode_possibleMoves_set)
    __swig_setmethods__["children"] = _UTTT.MonteCarloNode_children_set
    __swig_getmethods__["children"] = _UTTT.MonteCarloNode_children_get
    if _newclass:
        children = _swig_property(_UTTT.MonteCarloNode_children_get, _UTTT.MonteCarloNode_children_set)
    __swig_setmethods__["move"] = _UTTT.MonteCarloNode_move_set
    __swig_getmethods__["move"] = _UTTT.MonteCarloNode_move_get
    if _newclass:
        move = _swig_property(_UTTT.MonteCarloNode_move_get, _UTTT.MonteCarloNode_move_set)
    __swig_setmethods__["childNum"] = _UTTT.MonteCarloNode_childNum_set
    __swig_getmethods__["childNum"] = _UTTT.MonteCarloNode_childNum_get
    if _newclass:
        childNum = _swig_property(_UTTT.MonteCarloNode_childNum_get, _UTTT.MonteCarloNode_childNum_set)
    __swig_setmethods__["N"] = _UTTT.MonteCarloNode_N_set
    __swig_getmethods__["N"] = _UTTT.MonteCarloNode_N_get
    if _newclass:
        N = _swig_property(_UTTT.MonteCarloNode_N_get, _UTTT.MonteCarloNode_N_set)
    __swig_setmethods__["T"] = _UTTT.MonteCarloNode_T_set
    __swig_getmethods__["T"] = _UTTT.MonteCarloNode_T_get
    if _newclass:
        T = _swig_property(_UTTT.MonteCarloNode_T_get, _UTTT.MonteCarloNode_T_set)
    __swig_setmethods__["heuristic"] = _UTTT.MonteCarloNode_heuristic_set
    __swig_getmethods__["heuristic"] = _UTTT.MonteCarloNode_heuristic_get
    if _newclass:
        heuristic = _swig_property(_UTTT.MonteCarloNode_heuristic_get, _UTTT.MonteCarloNode_heuristic_set)
    __swig_setmethods__["ID"] = _UTTT.MonteCarloNode_ID_set
    __swig_getmethods__["ID"] = _UTTT.MonteCarloNode_ID_get
    if _newclass:
        ID = _swig_property(_UTTT.MonteCarloNode_ID_get, _UTTT.MonteCarloNode_ID_set)

    def __init__(self):
        this = _UTTT.new_MonteCarloNode()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_MonteCarloNode
    __del__ = lambda self: None
MonteCarloNode_swigregister = _UTTT.MonteCarloNode_swigregister
MonteCarloNode_swigregister(MonteCarloNode)

class RolloutArg(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, RolloutArg, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, RolloutArg, name)
    __repr__ = _swig_repr
    __swig_setmethods__["game"] = _UTTT.RolloutArg_game_set
    __swig_getmethods__["game"] = _UTTT.RolloutArg_game_get
    if _newclass:
        game = _swig_property(_UTTT.RolloutArg_game_get, _UTTT.RolloutArg_game_set)
    __swig_setmethods__["player"] = _UTTT.RolloutArg_player_set
    __swig_getmethods__["player"] = _UTTT.RolloutArg_player_get
    if _newclass:
        player = _swig_property(_UTTT.RolloutArg_player_get, _UTTT.RolloutArg_player_set)
    __swig_setmethods__["policy"] = _UTTT.RolloutArg_policy_set
    __swig_getmethods__["policy"] = _UTTT.RolloutArg_policy_get
    if _newclass:
        policy = _swig_property(_UTTT.RolloutArg_policy_get, _UTTT.RolloutArg_policy_set)
    __swig_setmethods__["seed"] = _UTTT.RolloutArg_seed_set
    __swig_getmethods__["seed"] = _UTTT.RolloutArg_seed_get
    if _newclass:
        seed = _swig_property(_UTTT.RolloutArg_seed_get, _UTTT.RolloutArg_seed_set)
    __swig_setmethods__["result"] = _UTTT.RolloutArg_result_set
    __swig_getmethods__["result"] = _UTTT.RolloutArg_result_get
    if _newclass:
        result = _swig_property(_UTTT.RolloutArg_result_get, _UTTT.RolloutArg_result_set)

    def __init__(self):
        this = _UTTT.new_RolloutArg()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _UTTT.delete_RolloutArg
    __del__ = lambda self: None
RolloutArg_swigregister = _UTTT.RolloutArg_swigregister
RolloutArg_swigregister(RolloutArg)


def countTopLeft(foo):
    return _UTTT.countTopLeft(foo)
countTopLeft = _UTTT.countTopLeft

def countTopCentre(foo):
    return _UTTT.countTopCentre(foo)
countTopCentre = _UTTT.countTopCentre

def countCentre(foo):
    return _UTTT.countCentre(foo)
countCentre = _UTTT.countCentre

def countFromStartWrapper(arg):
    return _UTTT.countFromStartWrapper(arg)
countFromStartWrapper = _UTTT.countFromStartWrapper

def countFromStartWrapperLayers(arg):
    return _UTTT.countFromStartWrapperLayers(arg)
countFromStartWrapperLayers = _UTTT.countFromStartWrapperLayers

def countFromStart(board, row, column):
    return _UTTT.countFromStart(board, row, column)
countFromStart = _UTTT.countFromStart

def countFromStartLayers(board, row, column, layers):
    return _UTTT.countFromStartLayers(board, row, column, layers)
countFromStartLayers = _UTTT.countFromStartLayers

def countTopLeftLayers(mLayers):
    return _UTTT.countTopLeftLayers(mLayers)
countTopLeftLayers = _UTTT.countTopLeftLayers

def countTopCentreLayers(mLayers):
    return _UTTT.countTopCentreLayers(mLayers)
countTopCentreLayers = _UTTT.countTopCentreLayers

def countCentreLayers(mLayers):
    return _UTTT.countCentreLayers(mLayers)
countCentreLayers = _UTTT.countCentreLayers

def createCGameState():
    return _UTTT.createCGameState()
createCGameState = _UTTT.createCGameState

def cloneCGameState(game):
    return _UTTT.cloneCGameState(game)
cloneCGameState = _UTTT.cloneCGameState

def freeCGameState(game):
    return _UTTT.freeCGameState(game)
freeCGameState = _UTTT.freeCGameState

def isValidMove(game, board, row, column):
    return _UTTT.isValidMove(game, board, row, column)
isValidMove = _UTTT.isValidMove

def isBoardWon(game, board, row, column):
    return _UTTT.isBoardWon(game, board, row, column)
isBoardWon = _UTTT.isBoardWon

def isGameWon(game, board):
    return _UTTT.isGameWon(game, board)
isGameWon = _UTTT.isGameWon

def playTurn(game, board, row, column):
    return _UTTT.playTurn(game, board, row, column)
playTurn = _UTTT.playTurn

def countMoves(game):
    return _UTTT.countMoves(game)
countMoves = _UTTT.countMoves

def countMovesLayers(game, layers):
    return _UTTT.countMovesLayers(game, layers)
countMovesLayers = _UTTT.countMovesLayers

def chooseMoveFullBoard(game):
    return _UTTT.chooseMoveFullBoard(game)
chooseMoveFullBoard = _UTTT.chooseMoveFullBoard

def chooseMoveSingleGrid(game, board):
    return _UTTT.chooseMoveSingleGrid(game, board)
chooseMoveSingleGrid = _UTTT.chooseMoveSingleGrid

def getMoves(game):
    return _UTTT.getMoves(game)
getMoves = _UTTT.getMoves

def revertTurn(game, board, row, column, previousBoard):
    return _UTTT.revertTurn(game, board, row, column, previousBoard)
revertTurn = _UTTT.revertTurn

def chooseMoveListSingleGrid(game, moves, board):
    return _UTTT.chooseMoveListSingleGrid(game, moves, board)
chooseMoveListSingleGrid = _UTTT.chooseMoveListSingleGrid

def chooseMoveListFullBoard(game, moves):
    return _UTTT.chooseMoveListFullBoard(game, moves)
chooseMoveListFullBoard = _UTTT.chooseMoveListFullBoard

def getMovesList(game, moves):
    return _UTTT.getMovesList(game, moves)
getMovesList = _UTTT.getMovesList

def shuffleMoveList(list):
    return _UTTT.shuffleMoveList(list)
shuffleMoveList = _UTTT.shuffleMoveList

def shuffleMoves(moves, moveCount):
    return _UTTT.shuffleMoves(moves, moveCount)
shuffleMoves = _UTTT.shuffleMoves

def trimMoves(moves, length):
    return _UTTT.trimMoves(moves, length)
trimMoves = _UTTT.trimMoves

def copyCGameState(copy, original):
    return _UTTT.copyCGameState(copy, original)
copyCGameState = _UTTT.copyCGameState

def evaluateBoard(game, val):
    return _UTTT.evaluateBoard(game, val)
evaluateBoard = _UTTT.evaluateBoard

def evaluateGrid(game, grid, val):
    return _UTTT.evaluateGrid(game, grid, val)
evaluateGrid = _UTTT.evaluateGrid

def staticHeuristic(game, val):
    return _UTTT.staticHeuristic(game, val)
staticHeuristic = _UTTT.staticHeuristic

def staticHeuristicWrapper(game, val):
    return _UTTT.staticHeuristicWrapper(game, val)
staticHeuristicWrapper = _UTTT.staticHeuristicWrapper

def minimax(game, depth, alpha, beta, maximize, heuristic, val):
    return _UTTT.minimax(game, depth, alpha, beta, maximize, heuristic, val)
minimax = _UTTT.minimax

def minimaxWrapper(game, depth, alpha, beta, maximize, val):
    return _UTTT.minimaxWrapper(game, depth, alpha, beta, maximize, val)
minimaxWrapper = _UTTT.minimaxWrapper

def evaluateAndRecordBoard(game, boardRelevance, val):
    return _UTTT.evaluateAndRecordBoard(game, boardRelevance, val)
evaluateAndRecordBoard = _UTTT.evaluateAndRecordBoard

def evaluateGridAndRecord(game, grid, winnable, val):
    return _UTTT.evaluateGridAndRecord(game, grid, winnable, val)
evaluateGridAndRecord = _UTTT.evaluateGridAndRecord

def playableBoardHeuristic(game, val):
    return _UTTT.playableBoardHeuristic(game, val)
playableBoardHeuristic = _UTTT.playableBoardHeuristic

def playableBoardHeuristicWrapper(game, val):
    return _UTTT.playableBoardHeuristicWrapper(game, val)
playableBoardHeuristicWrapper = _UTTT.playableBoardHeuristicWrapper

def randomMove(game):
    return _UTTT.randomMove(game)
randomMove = _UTTT.randomMove

def chooseRandomMove(game, moves):
    return _UTTT.chooseRandomMove(game, moves)
chooseRandomMove = _UTTT.chooseRandomMove

def chooseWinningMove(game, moves):
    return _UTTT.chooseWinningMove(game, moves)
chooseWinningMove = _UTTT.chooseWinningMove

def chooseWinLose(game, moves):
    return _UTTT.chooseWinLose(game, moves)
chooseWinLose = _UTTT.chooseWinLose

def simulateGame(game, policy):
    return _UTTT.simulateGame(game, policy)
simulateGame = _UTTT.simulateGame

def monteCarloHeuristic(game, val):
    return _UTTT.monteCarloHeuristic(game, val)
monteCarloHeuristic = _UTTT.monteCarloHeuristic

def monteCarloHeuristicWrapper(game, val):
    return _UTTT.monteCarloHeuristicWrapper(game, val)
monteCarloHeuristicWrapper = _UTTT.monteCarloHeuristicWrapper

def getHeuristicDouble(game, args, player):
    return _UTTT.getHeuristicDouble(game, args, player)
getHeuristicDouble = _UTTT.getHeuristicDouble

def monteCarloTreeSearch(game, args):
    return _UTTT.monteCarloTreeSearch(game, args)
monteCarloTreeSearch = _UTTT.monteCarloTreeSearch

def intializeRoot(root, game, args, player):
    return _UTTT.intializeRoot(root, game, args, player)
intializeRoot = _UTTT.intializeRoot

def createNode(game, parent, move, args, player):
    return _UTTT.createNode(game, parent, move, args, player)
createNode = _UTTT.createNode

def expand(node, args, player):
    return _UTTT.expand(node, args, player)
expand = _UTTT.expand

def traverse(node, args, player):
    return _UTTT.traverse(node, args, player)
traverse = _UTTT.traverse

def calcUCB(node, args):
    return _UTTT.calcUCB(node, args)
calcUCB = _UTTT.calcUCB

def rollout(node, player, args):
    return _UTTT.rollout(node, player, args)
rollout = _UTTT.rollout

def backpropogate(node, result):
    return _UTTT.backpropogate(node, result)
backpropogate = _UTTT.backpropogate

def freeMonteCarloTree(root):
    return _UTTT.freeMonteCarloTree(root)
freeMonteCarloTree = _UTTT.freeMonteCarloTree

def freeMonteCarloNode(node):
    return _UTTT.freeMonteCarloNode(node)
freeMonteCarloNode = _UTTT.freeMonteCarloNode

def rollout_thread(r_arg):
    return _UTTT.rollout_thread(r_arg)
rollout_thread = _UTTT.rollout_thread

def simulateGame_thread(game, policy, buf):
    return _UTTT.simulateGame_thread(game, policy, buf)
simulateGame_thread = _UTTT.simulateGame_thread

def chooseWinLose_thread(game, moves, buf):
    return _UTTT.chooseWinLose_thread(game, moves, buf)
chooseWinLose_thread = _UTTT.chooseWinLose_thread

def chooseWinningMove_thread(game, moves, buf):
    return _UTTT.chooseWinningMove_thread(game, moves, buf)
chooseWinningMove_thread = _UTTT.chooseWinningMove_thread

def chooseRandomMove_thread(game, moves, buf):
    return _UTTT.chooseRandomMove_thread(game, moves, buf)
chooseRandomMove_thread = _UTTT.chooseRandomMove_thread

def monteCarloHeuristic_thread(args):
    return _UTTT.monteCarloHeuristic_thread(args)
monteCarloHeuristic_thread = _UTTT.monteCarloHeuristic_thread

def getID(game):
    return _UTTT.getID(game)
getID = _UTTT.getID

def setID(node):
    return _UTTT.setID(node)
setID = _UTTT.setID

def updateRoot(game, prev_root):
    return _UTTT.updateRoot(game, prev_root)
updateRoot = _UTTT.updateRoot

def initialize():
    return _UTTT.initialize()
initialize = _UTTT.initialize

def freeTree(prev_root):
    return _UTTT.freeTree(prev_root)
freeTree = _UTTT.freeTree

def freeUnused(node, ID):
    return _UTTT.freeUnused(node, ID)
freeUnused = _UTTT.freeUnused

def monteCarloTreeSearch_sf(game, args, prev_root):
    return _UTTT.monteCarloTreeSearch_sf(game, args, prev_root)
monteCarloTreeSearch_sf = _UTTT.monteCarloTreeSearch_sf

def intializeRoot_sf(root, game, args, player):
    return _UTTT.intializeRoot_sf(root, game, args, player)
intializeRoot_sf = _UTTT.intializeRoot_sf
# This file is compatible with both classic and new-style classes.


